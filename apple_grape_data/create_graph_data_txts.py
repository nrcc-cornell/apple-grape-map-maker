import aiohttp
import datetime
import json
import os
import numpy as np

from fetch import fetch_data_from
from handle_grape_data import handle_grape_data, grapes

async def create_graph_data_txts(start_date, target_dir, coords, limit):
    # Use earlier of season start or 40 days ago for start date
    sub_days = start_date - datetime.timedelta(days=60)
    season_start = datetime.datetime(start_date.year - (1 if start_date.month < 9 else 0), 8, 31)
    acis_start_date = (sub_days if sub_days < season_start else season_start).strftime('%Y-%m-%d')

    # Set up rest of API args
    acis_end_date = start_date.strftime('%Y-%m-%d')
    acis_input_dict = {"loc":coords,"sdate":acis_start_date,"edate":acis_end_date,"grid":"nrcc-model","elems":[{"name":"maxt"},{"name":"mint"}, {"name":"avgt"}]}
    acis_url = 'https://grid2.rcc-acis.org/GridData'

    # Get data from API
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(sock_read=15)) as session:
        try:
            data = await fetch_data_from(session, limit, acis_url, acis_input_dict)
            if -999 in data['data'][-1]: data['data'].pop(-1)
            data = np.array(data['data'])
        except Exception:
            print('Failed to get graph data')
            return None
    
    # Gather data to convenient format
    models = handle_grape_data(data[:,3].astype(float), graph=True)
    dates = data[:,0][-30:]
    maxts = data[:,1][-30:].astype(float)
    mints = data[:,2][-30:].astype(float)

    # Write data to files
    for grape in grapes:
        name = grape['name']
        with open(os.path.join(target_dir, 'grape', 'graph', f'{name}_data.json'), 'w') as f:
            json.dump({
                'dates': dates.tolist(),
                'min_temps': mints.tolist(),
                'max_temps': maxts.tolist(),
                'hardiness_temps': models[name]
            }, f)
