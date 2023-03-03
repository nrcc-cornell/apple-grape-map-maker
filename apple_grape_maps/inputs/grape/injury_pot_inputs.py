import sys

name = sys.argv[2]
title = sys.argv[3]
input_path = sys.argv[4]
output_path = sys.argv[5]

map_input = {
	'area': 'northeast',
	'outputfile': output_path,
	'maptype': 'colormesh',
	'gridsize': 8,
	'title': title,
  'title2': 'Bud Injury Potential\n',
  'titleyoffset': 0.13,
  'titlexoffset': 0.17,
	'datesfromfile': True,
	'inputfile': input_path,
	'contourbounds': [-999,0,0.50001,1.99999,999],
  'cbarsettings': [0.16, 0.11, 0.7, 0.02],
  'colorbarticklabelsize': 6,
  'categoricallegend': True,
  'keylabels': ['No Potential', 'Low', 'Medium', 'High'],
	'colors': [
    '#dddddd',
    '#1e90ff',
    '#ffd700',
    '#ff0000'
  ]
}
