import multiprocessing as mp
import subprocess
import os
import json
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt

# Announce completion of a map
def say_done(name):
  print(name, 'is done!')

def construct_name_and_title(file_name, extra_words=[]):
  words = file_name.split('_')
  
  # Ignores 'f#' if necessary
  if len(words[0]) == 2:
    words = words[1:-1]
  else:
    words = words[:-1]

  name = '_'.join(words)
  if '.npy' in file_name:
    title = f'GDD Difference from {" ".join(list(map(lambda word: word.capitalize(), words)))} ({extra_words[0]})'
  else:
    words = words + extra_words
    title = ' '.join(list(map(lambda word: word.capitalize(), words)))
  return name, title

grapes = ['cabernet_franc', 'concord', 'riesling']

def make_graph(data_dir, output_dir):
  for grape in grapes:
    # Load data
    with open(os.path.join(data_dir, f'{grape}_data.json')) as f:
      data_dict = json.load(f)

    # Convert data to more convenient forms
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in data_dict['dates']]
    start_date = dates[0].strftime('%B %d, %Y')
    end_date = dates[-1].strftime('%B %d, %Y')
    dates = [d.strftime('%-m/%-d') for d in dates]
    min_temps = data_dict['min_temps']
    max_temps = data_dict['max_temps']
    hardiness_temps = data_dict['hardiness_temps']
    grape_name = ' '.join([s.capitalize() for s in grape.split('_')])

    # Instantiate figure
    fig = plt.figure(figsize=((6.8, 6.55)))

    # Add min and max temps to graph
    plt.plot(dates, min_temps, color='blue', linewidth=1, label='Min Temp')
    plt.plot(dates, max_temps, color='blue', linewidth=1, label='Max Temp')
    plt.fill_between(dates, min_temps, max_temps, color=(0.2,0.2,1,0.3))
    
    # Add hardiness temps to graph
    plt.plot(dates, hardiness_temps, color='red', linewidth=1, label='Hardiness')

    # Format x-axis
    plt.xticks(range(4, len(dates), 5))
    plt.xlim([0,len(dates) - 1])
    plt.xlabel('Date')

    # Format y-axis
    plt.yticks(range(-20, 61, 20))
    plt.ylim([-30, 70])
    plt.ylabel('Temperature °F')

    # Add gridlines
    plt.grid(color = (0.5,0.5,0.5,1), linestyle = ':', dashes=(1,3))

    # Add title
    plt.title(f'{grape_name} at Geneva, NY\nModeled Hardiness Temp vs Observed Temp\n{start_date} thru {end_date}')

    # Add legend
    plt.legend(loc='upper right')

    # Save graph
    plt.savefig(os.path.join(output_dir, f'{grape}_graph.png'))
  
  # For callback
  return 'Graphing'

def make_elems_map(mapper_loc, date, output_path, options_path):
  # make the map
  subprocess.call([
    'python',
    mapper_loc,
    date,
    date,
    output_path,
    options_path
  ])

  return options_path.split('/')[-1] + ' elems map'

def make_basic_map(input_folder_path, output_folder_path, file_name, date_arg, options_path, mapper_loc, title_extras=[]):
  # set up args
  in_file = os.path.join(input_folder_path, file_name)
  map_name = file_name[:-8] + 'map.png'
  out_file = os.path.join(output_folder_path, map_name)
  name, title = construct_name_and_title(file_name, title_extras)
  
  # make the map
  subprocess.call([
    'python',
    mapper_loc,
    date_arg,
    name,
    title,
    in_file,
    out_file,
    options_path
  ])

  # for callback
  return out_file.split('/')[-1]

def create_maps(this_dir_path, mapper_loc, file_structure):
  # Initial set up
  today = date.today()
  base_output_dir = os.path.join(this_dir_path, 'maps')
  base_input_dir = os.path.join(this_dir_path, 'data_txts')

  # Set up multiprocessing
  num_workers = mp.cpu_count()
  pool = mp.Pool(num_workers)

  for project, folders in file_structure.items():
    project_path = os.path.join(base_output_dir, project)
    if not os.path.exists(project_path):
      os.mkdir(project_path)
    for folder in folders:
      output_folder_path = os.path.join(project_path, folder)
      if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)
      
      # 'stage' relies on gdd data so the gdd data, so the input file must be changed
      if folder == 'stage':
        input_folder_path = os.path.join(base_input_dir, project, 'gdds')
      else:
        input_folder_path = os.path.join(base_input_dir, project, folder)

      options_path = os.path.join('apple_grape_maps', 'inputs', project, folder)

      if folder == 'graph':
        pool.apply_async(make_graph, args=(input_folder_path, output_folder_path), callback=say_done)
      elif folder == 'low_temp':
        pool.apply_async(make_elems_map, args=(mapper_loc, today.strftime('%Y,%-m,%-d'), os.path.join(output_folder_path, 'low_temp_map.png'), options_path), callback=say_done)
      else:
        file_list = os.listdir(input_folder_path)
        for file_name in file_list:
          # Handles adjusting the map date to match the file (i.e. f2 is tomorrow)
          try:
            file_date = today + timedelta(days=int(file_name[1]) - 1)
          except:
            file_date = today
          file_date = '{0},{1},{2}'.format(file_date.year, file_date.month, file_date.day)
          
          # Handles adjusting the titles
          title_extras = []
          if folder == 'gdds' or folder == 'stage' or folder == 'kill_prob':
            title_extras = ['apple']

          pool.apply_async(make_basic_map, args=(input_folder_path, output_folder_path, file_name, file_date, options_path, mapper_loc, title_extras), callback=say_done)
  pool.close()
  pool.join()

def main():
  start_date = datetime.now()
  files = {
    'apple': ['chill','gdds','stage','kill_prob'],
    'grape': ['hardiness', 'injury_pot', 'graph', 'low_temp'],
  }
  base_dir = '/'
  mapper_loc = '/main/gridMapper.py'
  create_maps(base_dir, mapper_loc, files)
  print('Content created in: ' + str(datetime.now() - start_date))

main()