# apple-grape-map-maker

Creates apple and grape maps for use on NRCC’s page in the “Analyses for Industry” tab.
(in production by Bill)

## Dependency

You must have a Docker container called `mapper:1` containing the code for the mapper program from `https://github.coecis.cornell.edu/be99/mapper`.

## Setup

There is one dockerfile, a fairly generic python3 image to load the current data.
NOTE: The `USER 1000:1000` line may need to be configured to your specific 'user id':'group id' in each dockerfile to avoid permissions errors.

Build the image using `docker build -t python_base:1 -f Dockerfile_python_base .`

## Usage
#### Run together
 - Execute `python run_apple_grape.py`.
 - The data will be stored in the `data_txts` directory.
 - The map images will be in the `maps` directory.
 - The animations will be in the `maps` directory.

#### Run individually
- Fetch the data `docker-compose run --rm apple_grape_data python apple_grape_data/main.py`
- Create the map images `docker compose run -u $(id -u) --rm apple_grape_maps python apple_grape_maps/create_maps.py`
- Create the animations `docker-compose run --rm apple_grape_animations python apple_grape_maps/animate_maps.py`
