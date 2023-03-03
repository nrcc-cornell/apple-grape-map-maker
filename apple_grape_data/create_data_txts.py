import asyncio
import datetime

from setup import setup
from create_from_locHourly import create_from_locHrly
from create_graph_data_txts import create_graph_data_txts

async def main():
    # Set up variables
    start_time = datetime.datetime.now()
    start_date = start_time
    target_dir, coordinate_lists, skip_dict = setup(start_date)

    # Limits number of concurrent API calls
    limit = asyncio.Semaphore(15)

    # Create lots of data_txts and a data dict to be used in create_gdd_based_data_txts
    avg_temp_grid = await create_from_locHrly(start_date, target_dir, coordinate_lists, skip_dict, limit)
    risk_done = datetime.datetime.now()

    # Create graph data_txts
    coords = '-77.0,42.875'  # Geneva, NY
    await create_graph_data_txts(start_date, target_dir, coords, limit)
    graph_done = datetime.datetime.now()

    # Log run times
    print(f'Apple/Grape data calculated in: {str(risk_done - start_time)}')
    print(f'Graph data calculated in: {str(graph_done - risk_done)}')

# Execute
asyncio.run(main())