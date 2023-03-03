import json, os
from urllib.request import urlopen, Request

def get_coordinates(path, bbox):
    # One off to get a list of lats and a list of lons for all Grid points in the northeast from the ACIS server
    # Fetch data
    req = Request('http://grid2.rcc-acis.org/GridData', json.dumps({"bbox":bbox,"date":"2022-08-05","grid":"nrcc-model","elems":[{"name":"pcpn","interval":[0,0,1]}],"meta":"ll"}).encode())
    response = urlopen(req)
    data_vals = json.loads(response.read().decode('utf-8'))

    # Convert to convenient form
    lons = data_vals['meta']['lon'][0]
    lats_matrix = data_vals['meta']['lat']
    lats = []
    for lat in lats_matrix:
        lats.append(lat[0])

    # Save to file
    file = open(path, 'w')
    file.write(json.dumps({ 'lats': lats, 'lons': lons }))
    file.close()

def clear_dir(data_sections, data_dir, start_date):
    for project, folders in data_sections.items():
        project_path = os.path.join(data_dir, project)
        if not os.path.exists(project_path):
            os.mkdir(project_path)
        for folder, files in folders.items():
            folder_path = os.path.join(project_path, folder)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            # Create each file and add the date to be used for the relevant maps
            for name in files:
                with open(os.path.join(folder_path, f'{name}_data.txt'), 'w') as f:
                    f.write(f"{start_date.strftime('%Y,%m,%d')}")

def setup(start_date):
    # Define necessary varaibles
    bbox = '-82.70,37.20,-66.90,47.60'
    this_file_dir = os.path.split(__file__)[0]
    grid_coords_path = os.path.join(this_file_dir, 'grid_coords.txt')
    skip_coords_path = os.path.join(this_file_dir, 'skip_coords.txt')
    target_dir = os.path.join(os.path.split(this_file_dir)[0], 'data_txts')
    data_sections = {
        'apple': {
            'chill': ['chill_accumulations'],
            'gdds': ['red_delicious', 'empire', 'mcIntosh'],
            'kill_prob': ['red_delicious', 'empire', 'mcIntosh']
        },
        'grape': {
            'hardiness': ['cabernet_franc', 'concord', 'riesling'],
            'injury_pot': ['cabernet_franc', 'concord', 'riesling'],
            'graph': []
        }
    }

    # Call to refresh output directory
    clear_dir(data_sections, target_dir, start_date)

    # Load coordinate lists or create them
    if not os.path.exists(grid_coords_path):
        get_coordinates(grid_coords_path, bbox)
    with open(grid_coords_path, 'r') as coords_file:
        coordinate_lists = json.loads(coords_file.read())
    
    # Load coordinates to skip or default to empty obj
    try:
        with open(skip_coords_path, 'r') as skip_f:
            skip_dict = json.load(skip_f)
    except:
        skip_dict = {}

    return target_dir, coordinate_lists, skip_dict
