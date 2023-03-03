import sys

input_path = sys.argv[4]
output_path = sys.argv[5]

map_input = {
	'area': 'northeast',
	'outputfile': output_path,
	'maptype': 'interpf',
	'title': 'Accumulated Chill',
  'titleyoffset': 0.13,
  'titlexoffset': 0.17,
	'datesfromfile': True,
	'inputfile': input_path,
	'contourbounds': [200,300,400,500,600,700,800,900,1000,1100,1200,1300],
	'colors': [
    '#5e0000',
    '#b20000',
    '#ff2900',
    '#ff8200',
    '#ffd700',
    '#c7ff30',
    '#7aff7d',
    '#30ffc7',
    '#00c5ff',
    '#0069ff',
    '#0008ff',
    '#0000b2',
    '#9999ff'
  ]
}
