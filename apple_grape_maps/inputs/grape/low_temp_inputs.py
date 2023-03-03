import sys

output_path = sys.argv[3]

map_input = {
	'area' : 'northeast',
	'outputfile' : output_path,
	'maptype' : 'contourf',
	'title' : 'Lowest Temperature Since July 1 (°F)',
	'elems' : [{
    "name":"mint",
    "interval":[0,0,1],
    "duration":"std",
    "season_start":[7,1],
    "reduce":"min"
  }],
	'grid' : '3',
	'contourbounds': [*range(15,51,5)]
}