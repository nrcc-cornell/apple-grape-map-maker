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
  'title2': 'Kill Probability\n',
  'titleyoffset': 0.13,
  'titlexoffset': 0.17,
	'datesfromfile': True,
	'inputfile': input_path,
	'contourbounds': [-999,0.9999,1.9999,2.9999,999],
  'cbarsettings': [0.16, 0.11, 0.7, 0.02],
  'colorbarticklabelsize': 6,
  'categoricallegend': True,
  'keylabels': ['0%', '10%', '50%', '90%'],
	'colors': [
    '#dddddd',
    '#1e90ff',
    '#ffd700',
    '#ff0000'
  ]
}
