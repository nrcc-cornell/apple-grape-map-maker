import subprocess
import os

# Scripts divided up because they rely on different Docker images

# Run script for data collection
subprocess.call([
  'docker-compose',
  'run',
  '--rm',
  'apple_grape_data',
  'python',
  'apple_grape_data/create_data_txts.py'
])

# Run script for map creation
subprocess.call([
  'docker',
  'compose',
  'run',
  '-u',
  str(os.getuid()),
  '--rm',
  'apple_grape_maps',
  'python',
  'apple_grape_maps/create_maps.py'
])

# Run script for animation creation
subprocess.call([
  'docker-compose',
  'run',
  '--rm',
  'apple_grape_animations',
  'python',
  'apple_grape_maps/animate_maps.py'
])