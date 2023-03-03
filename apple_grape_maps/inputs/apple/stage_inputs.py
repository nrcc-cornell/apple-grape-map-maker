import sys

name = sys.argv[2]
title = sys.argv[3]
input_path = sys.argv[4]
output_path = sys.argv[5]

# bounds = ['stip','gtip','ghalf','cluster','pink','bloom','petalfall']
if name == 'empire':
  bounds = [0,97,132,192,248,331,424,539,99999]
elif name == 'mcIntosh':
  bounds = [0,91,107,170,224,288,384,492,99999]
elif name == 'red_delicious':
  bounds = [0,85,121,175,233,295,382,484,99999]

map_input = {
	'area': 'northeast',
	'outputfile': output_path,
	'maptype': 'colormesh',
	'gridsize': 8,
	'title': title,
  'title2': 'Phenological Stages\n',
  'titleyoffset': 0.13,
  'titlexoffset': 0.17,
	'datesfromfile': True,
	'inputfile': input_path,
	'contourbounds': bounds,
  'cbarsettings': [0.16, 0.11, 0.7, 0.02],
  'colorbarticklabelsize': 6,
  'categoricallegend': True,
  'keylabels': ['Dormant', 'Silver Tip','Green Tip','1/2" Green','Tight Cluster','Pink Bud','Bloom','Petal Fall'],
	'colors': [
    '#ffebcd',
    '#c0c0c0',
    '#32cd32',
    '#008000',
    '#87ceeb',
    '#ff00ff',
    '#ffff00',
    '#ff0000'
  ]
}
