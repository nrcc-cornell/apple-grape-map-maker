import os
from PIL import Image, ImageSequence
import multiprocessing as mp
import moviepy.editor as mov
from datetime import datetime

def make_animations(dir, name, map_type):
  is_feb_thru_july = map_type in ['gdds','stage','kill_prob']
  is_sept_to_sept = map_type == 'chill'
  is_dec_thru_june = map_type == 'hardiness'
  is_oct_thru_june = map_type == 'injury_pot'

  # Dont add to animation if out of season
  today = datetime.now()
  if (is_feb_thru_july and (today.month == 1 or today.month > 7)) or (is_dec_thru_june and (7 <= today.month <= 11)) or (is_oct_thru_june and (7 <= today.month <= 9)):
    return 'Out of Season, not added to animation'

  # Define file locations
  map_path = os.path.join(dir, name + '_map.png')
  gif_path = os.path.join(dir, name + '_map.gif')
  mp4_path = os.path.join(dir, name + '_map.mp4')

  # Get new map and resize it to keep file size low
  with Image.open(map_path) as im:
    im = im.resize((544, 524))
  
  # Add new map to gif or create gif if there isn't one
  try:
    # Raise error to force refresh the animation at the beginning of the season
    if (today.day == 1 and ((is_feb_thru_july and today.month == 2) or (is_dec_thru_june and today.month == 12) or (is_oct_thru_june and today.month == 10) or (is_sept_to_sept and today.month == 9))):
      raise 'Restart GIF'
    
    with Image.open(gif_path) as animation:
      frames = ImageSequence.all_frames(animation)
      
      ########################################
      ########################################
      ### THIS IS A ONE-TIME EXECUTION SECTION
      ###   THAT IS MEANT TO SHORTEN A GIF FROM
      ###   OVER ONE YEAR OF MAPS TO JUST THE
      ###   CURRENT YEARS MAPS. THIS SHOULD
      ###   ONLY EXECUTE ONCE IN MARCH OF 2024
      ###   AND CAN THEN BE REMOVED IN A LATER
      ###   UPDATE!
      ########################################
      ########################################

      if len(frames) > 370 and today.month == 3 and today.year == 2024:
        if is_feb_thru_july :
          frames = frames[331:]
        elif is_dec_thru_june:
          frames = frames[269:]
        elif is_oct_thru_june:
          frames = frames[208:]
        elif is_sept_to_sept:
          frames = frames[178:]

      ########################################
      ########################################

      # Add frame on first run of day (10:15am EST), otherwise replace last frame
      if 15 < datetime.utcnow().hour:
        frames.pop()
      
      frames.append(im)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=250, loop=0)
  except:
    im.save(gif_path, save_all=True, append_images=[im], duration=250, loop=0)

  # Convert gif to mp4 to make file smaller for web use
  gif = mov.VideoFileClip(gif_path)
  gif.write_videofile(mp4_path, logger=None)

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
        if (folder == 'chill' and species != 'chill_accumulations') or (species == 'chill_accumulations' and folder != 'chill'):
          continue
        pool.apply_async(make_animations, args=(folder_path, species, folder))

  # End multiprocessing
  pool.close()
  pool.join()
  
  print('Animations created in: ' + str(datetime.now() - start))



main()
