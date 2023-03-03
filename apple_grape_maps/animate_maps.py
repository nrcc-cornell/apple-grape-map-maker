import os
from PIL import Image, ImageSequence
import multiprocessing as mp
import moviepy.editor as mov
from datetime import datetime

# Announce completion of a map
def say_done(name):
  print(name, 'is animated!')

def make_animations(dir, name):
  # Define file locations
  map_path = os.path.join(dir, name + '_map.png')
  gif_path = os.path.join(dir, name + '_map.gif')
  mp4_path = os.path.join(dir, name + '_map.mp4')

  # Get new map and resize it to keep file size low
  with Image.open(map_path) as im:
    im = im.resize((544, 524))
  
  # Add new map to gif or create gif if there isn't one
  try:
    with Image.open(gif_path) as animation:
      frames = ImageSequence.all_frames(animation)
      
      # Add frame on first run of day (10:15am EST), otherwise replace last frame
      if 15 < datetime.utcnow().hour:
        frames.pop()
      
      frames.append(im)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=250, loop=0)
  except Exception as e:
    im.save(gif_path, save_all=True, append_images=[im], duration=250, loop=0)

  # Convert gif to mp4 to make file smaller for web use
  gif = mov.VideoFileClip(gif_path)
  gif.write_videofile(mp4_path, logger=None)
  
  return name

def main():
  # Initial set up
  start = datetime.now()
  base_dir = '/'
  file_structure = {
    'apple': {
      'folders': ['chill','gdds','stage','kill_prob'],
      'species': ['chill_accumulations', 'empire', 'mcIntosh', 'red_delicious']
    },
    'grape': {
      'folders': ['hardiness', 'injury_pot'],
      'species': ['cabernet_franc', 'concord', 'riesling']
    }
  }
  
  content_dir = os.path.join(base_dir, 'maps')

  # Set up multiprocessing
  num_workers = mp.cpu_count()
  pool = mp.Pool(num_workers)

  for project, contents in file_structure.items():
    project_path = os.path.join(content_dir, project)
    species_list = contents['species']
    for folder in contents['folders']:
      folder_path = os.path.join(project_path, folder)
      for species in species_list:
        pool.apply_async(make_animations, args=(folder_path, species), callback=say_done)

  # End multiprocessing
  pool.close()
  pool.join()
  
  print('Animations created in: ' + str(datetime.now() - start))



main()
