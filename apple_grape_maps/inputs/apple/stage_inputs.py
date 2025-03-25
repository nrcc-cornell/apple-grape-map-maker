import sys

name = sys.argv[2]
title = sys.argv[3]
input_path = sys.argv[4]
output_path = sys.argv[5]

# bounds = ['stip','gtip','ghalf','cluster','pink','bloom','petalfall']
if name == 'empire':
  bounds = [0,97,103,186,233,297,393,500,99999]
elif name == 'mcIntosh':
  bounds = [0,85,122,178,233,294,385,484,99999]
elif name == 'red_delicious':
  bounds = [0,97,137,195,248,336,433,550,99999]

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
