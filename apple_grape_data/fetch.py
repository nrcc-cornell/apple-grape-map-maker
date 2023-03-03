import json


async def fetch_data(session, url, elems):
    # Fetch data from given API
    async with session.post(url, json=elems) as resp:
        return json.loads(await resp.text())


async def fetch_data_from(session, limit, url, input_dict):
    # Tries to get gata from API twice before giving up
    async with limit:
        ep = url.split('/')[-1]
        try:
            data_vals = await fetch_data(session, url, input_dict)
        except:
            try:
                data_vals = await fetch_data(session, url, input_dict)
            except:
                return None
        return data_vals
