import datetime, os, math
import asyncio
import aiohttp
import numpy as np
from scipy.interpolate import splrep, splev

from fetch import fetch_data_from
from handle_apple_data import handle_apple_data
from handle_grape_data import handle_grape_data

def chill_value(deg_f):
    # Convert temp in F to hourly chill units
    if deg_f <= 34.7:  return 0
    if deg_f <= 44.78: return 0.5
    if deg_f <= 55.22: return 1
    if deg_f <= 61.52: return 0.5
    if deg_f <= 66.02: return 0
    if deg_f <= 69.08: return -0.5
    if deg_f <= 71.6:  return -1
    if deg_f <= 73.76: return -1.5
    if deg_f >  73.76: return -2

def baskerville_emin(mint, maxt, baset):
  avgt = (mint + maxt) / 2
  if mint >= baset:
    dd = max(avgt - baset, 0)
  elif maxt <= baset:
    dd = 0
  else:
    tamt = (maxt - mint) /  2
    t1 = math.asin((baset - avgt) /  tamt)
    dd =  round(max((((tamt * math.cos(t1)) - ((baset - avgt) * ((3.14 / 2.0) - t1))) / 3.14), 0), 2)
  return dd

def acis_to_data_txts(data, lon, lat, target_dir):
    # Convert data to numpy array because it is much faster, use it to group data and calculate a spline function
    np_data = np.array(data['data'])
    dates = np_data[:,0]
    v_be = np.vectorize(baskerville_emin)
    gdds = v_be(np_data[:,2].astype(float), np_data[:,1].astype(float), 43)
    temps = np.column_stack((np_data[:,2],np_data[:,1])).flatten().astype(int)
    xs = np.arange(0, len(temps) * 12, 12)
    curve = splrep(xs, temps)

    # Use spline function to calculate chill and gdd sums. Threshold grows as it is exceeded to trigger gdds to start accumulating when necessary
    sums = {
        'chill_accumulations': 0,
        'gdd_accumulations_1000': 0,
        'gdd_accumulations_1100': 0
    }
    threshold = 1000
    for date_idx in range(1, len(dates) - 1):
        start_hr_idx = date_idx * 24
        temps = splev(range(start_hr_idx, start_hr_idx + 24), curve)
        for temp in temps:
            hr_chill = chill_value(temp)
            sums['chill_accumulations'] = max(0, sums['chill_accumulations'] + hr_chill)
        
        if sums['chill_accumulations'] > 1000 or threshold > 1000:
            if threshold == 1000:
                threshold = 1100
            else:
                sums['gdd_accumulations_1000'] += gdds[date_idx]
        
        if sums['chill_accumulations'] > 1100 or threshold > 1100:
            if threshold == 1100:
                threshold = 2000
            else:
                sums['gdd_accumulations_1100'] += gdds[date_idx]

    # Write to chill file
    with open(os.path.join(target_dir, 'apple', 'chill', 'chill_accumulations_data.txt'), 'a') as f:
        f.write(f'\n\t{lat}\t{lon}\t{sums["chill_accumulations"]}')

    # Write gdds and kill_probs to individual apple files
    handle_apple_data(target_dir, lat, lon, sums, int(np_data[-1][2]))

    #Write grape hardiness to grape files
    handle_grape_data(np_data[:,3][1:-1].astype(float), target_dir, lat, lon, float(np_data[-2][2]))


async def gather_data(session, limit, lat, lon, start_date, fail_list):
    # Set up for locHrly call
    locHrly_start_date = datetime.datetime.now().strftime('%Y%m%d') + '08'
    locHrly_input_dict = {"lon": lon, "lat": lat, "tzo": -5, "sdate": locHrly_start_date, "edate": "now"}
    locHrly_url = 'https://hrly.nrcc.cornell.edu/locHrly'

    # Set up for ACIS call
    acis_start_date = str(start_date.year - (1 if start_date.month < 9 else 0)) + '-08-31'
    acis_end_date = start_date.strftime('%Y-%m-%d')
    acis_input_dict = {"loc":str(lon) + ',' + str(lat),"sdate":acis_start_date,"edate":acis_end_date,"grid":"nrcc-model","elems":[{"name":"maxt"},{"name":"mint"}, {"name":"avgt"}]}
    acis_url = 'https://grid2.rcc-acis.org/GridData'
    
    # Attempt to get data from both APIs, if either fail or timeout (set when ClientSession is created) store coordinates for showing failures and return empty results
    try:
        locHrly_data, acis_data = await asyncio.gather(
            fetch_data_from(session, limit, locHrly_url, locHrly_input_dict),
            fetch_data_from(session, limit, acis_url, acis_input_dict)
        )
        if not locHrly_data or not acis_data: raise Exception('Failed to get data for: ', lat, lon)
    except asyncio.exceptions.TimeoutError:
        print('Timeout trying to get: ', lat, lon)
        fail_list.append([lat,lon])
        return None, None
    except Exception as e:
        print(e)
        fail_list.append([lat,lon])
        return None, None
    
    # If last entry in ACIS data is missing, get rid of it
    if -999 in acis_data['data'][-1]:
        acis_data['data'].pop(-1)

    # Add first forecast to ACIS to be used in the spline calculation
    acis_data['data'] = acis_data['data'] + [[day[0], round(float(day[1])), round(float(day[2])), 0] for day in [locHrly_data['dlyFcstData'][0]]]
    return acis_data


async def process_point(session, limit, lat, lon, start_date, target_dir, fail_list):
    # Try to get data for the point, if any error occurs return empty results
    try:
        acis_data = await gather_data(session, limit, lat, lon, start_date, fail_list)
        acis_to_data_txts(acis_data, lon, lat, target_dir)
    except:
        return None


async def create_from_locHrly(start_date, target_dir, coordinate_lists, skip_dict, limit):
    # Creates data files for all risk indices and returns a numpy grid of forecasted gdds
    fail_list = []
    
    # Step of 2 to make an 8km grid instead of a 4km grid
    for lat_idx in range(0, len(coordinate_lists['lats']), 2):
        latitude = coordinate_lists['lats'][lat_idx]
        print('Starting latitude: ', latitude)

        s = datetime.datetime.now()
                
        try:
            skip_list = skip_dict[str(latitude)]
        except:
            skip_list = []
        
        good_lons = []
        # Step of 2 to make an 8km grid instead of a 4km grid
        for lon_idx in range(0, len(coordinate_lists['lons']), 2):
            if not coordinate_lists['lons'][lon_idx] in skip_list:
                good_lons.append(coordinate_lists['lons'][lon_idx])

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(sock_read=15)) as session:
            pnt_cors = [process_point(session, limit, latitude, longitude, start_date, target_dir, fail_list) for longitude in good_lons]
            await asyncio.gather(*pnt_cors)
        
        print('End: ', str(datetime.datetime.now() - s))
    print('Failed: ', fail_list)
    print(len(fail_list))
