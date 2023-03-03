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
  'title2': 'Accumulated Growing Degree Days\n',
  'titleyoffset': 0.13,
	'datesfromfile': True,
	'inputfile': input_path,
	'contourbounds': [25, 125, 225, 325, 475, 525, 625, 725],
	'colors': [
    '#000080',
    '#0000d1',
    '#0059ff',
    '#06edf1',
    '#9aff5d',
    '#ffdb00',
    '#ff7300',
    '#d10000',
    '#800000'
  ]
}
