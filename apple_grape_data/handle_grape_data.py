import os

# GLOBALS
grapes = [{
        'name': 'cabernet_franc',
        'hardiness': {
            'init':-9.9,
            'min':-1.2,
            'max':-25.4,
        },
        'tempThresh':[13.0,4.0],
        'dormBoundary':-500,
        'acclimRate':[0.12,0.10],
        'deacclimRate':[0.04,0.10],
        'theta':7
    },{
        'name': 'concord',
        'hardiness': {
            'init':-12.8,
            'min':-2.5,
            'max':-29.5,
        },
        'tempThresh':[13.0,3.0],
        'dormBoundary':-600,
        'acclimRate':[0.12,0.10],
        'deacclimRate':[0.02,0.10],
        'theta':3
    },{
        'name':'riesling',
        'hardiness': {
            'init':-12.6,
            'min':-1.2,
            'max':-26.1,
        },
        'tempThresh':[12.0,5.0],
        'dormBoundary':-700,
        'acclimRate':[0.14,0.10],
        'deacclimRate':[0.02,0.12],
        'theta':7
    }]

def calc_gdd(avgTemp, thres): return avgTemp - thres if avgTemp > thres else 0
def calc_chill_dd(avgTemp, thres): return avgTemp - thres if avgTemp < thres else 0

def handle_grape_data(avg_temps, target_dir=None, lat=None, lon=None, min_temp=None, graph=False):
    # Initialize models only if we want graph data
    models = {} if graph else None

    for grape in grapes:
        max_h = grape['hardiness']['max']
        min_h = grape['hardiness']['min']
        hardiness_range = min_h - max_h
        yesterday_hardiness = grape['hardiness']['init']
        hardiness_model = []
        period = 0
        chilling_Sum = 0
        dd10_sum = 0

        for temp in avg_temps:
            heat = calc_gdd(temp, grape['tempThresh'][period])
            chill = calc_chill_dd(temp, grape['tempThresh'][period])
            dd10 = calc_chill_dd(temp, 10.0)

            new_chill = heat * grape['deacclimRate'][period] * (1 - pow((yesterday_hardiness - max_h) / hardiness_range, grape['theta']))
            new_heat = chill * grape['acclimRate'][period] * (1 - (min_h - yesterday_hardiness) / hardiness_range)

            new_hardiness = yesterday_hardiness + new_chill + new_heat
            if new_hardiness <= max_h: new_hardiness = max_h
            if new_hardiness > min_h: new_hardiness = min_h
            hardiness_model.append(round(new_hardiness * (9/5) + 32, 1))
            yesterday_hardiness = new_hardiness

            chilling_Sum += chill

            dd10_sum += dd10
            if dd10_sum <= grape['dormBoundary']: period = 1

        if models == None:
            # Write hardiness_temp to file
            with open(os.path.join(target_dir, 'grape', 'hardiness', f'{grape["name"]}_data.txt'), 'a') as f:
                f.write(f'\n\t{lat}\t{lon}\t{hardiness_model[-1]}')

            # Write injury_pot to file
            injury_pot = hardiness_model[-1] - min_temp
            with open(os.path.join(target_dir, 'grape', 'injury_pot', f'{grape["name"]}_data.txt'), 'a') as f:
                f.write(f'\n\t{lat}\t{lon}\t{injury_pot}')
        else:
            # Store last 30 days of hardiness temps for graph
            models[grape['name']] = hardiness_model[-30:]
    return models