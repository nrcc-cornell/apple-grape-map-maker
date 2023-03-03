import sys

title = sys.argv[3]
input_path = sys.argv[4]
output_path = sys.argv[5]

map_input = {
	'area': 'northeast',
	'outputfile': output_path,
	'maptype': 'colormesh',
	'gridsize': 8,
	'title': title,
  'title2': 'Modeled Hardiness Temperature (°F)\n',
  'titleyoffset': 0.13,
  'colorbarticklabelsize': 6,
	'datesfromfile': True,
	'inputfile': input_path,
	'contourbounds': [val/10 for val in range(-250,301,25)],   # -25 to 30, every 2.5
	'colors': [
    '#000080',
    '#000096',
    '#0000cd',
    '#0000ff',
    '#0021ff',
    '#0051ff',
    '#0081ff',
    '#00adff',
    '#00ddfe',
    '#1cffdb',
    '#43ffb4',
    '#69fe8c',
    '#8dff6a',
    '#b4ff43',
    '#dbff1c',
    '#feed00',
    '#ffc100',
    '#ff9400',
    '#ff6c00',
    '#ff3f00',
    '#ff1600',
    '#cd0000',
    '#960000',
    '#800000'
  ]
}
