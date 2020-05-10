import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor

try:
    from src import settings
    from src.utils import filter_data, filter_resources
    
except ModuleNotFoundError:
    import settings
    from utils import filter_data, filter_resources


def get_request_results(session, resource, page=1):
    url = f'{settings.BASE_URL}{resource}/?page={page}'
    with session.get(url) as response:
        if response.status_code != 200:
            raise Exception

        return response.json()['results']


async def get_all():
    resources = {
        'people': {},
        'starships': {},
        'vehicles': {},
        'planets': {},
        'films': {},
    }
    with ThreadPoolExecutor(max_workers=4) as executor:
        for resource in settings.RESOURCES:
            pages = settings.PAGES[resource]
        
            with requests.Session() as session:
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        get_request_results,
                        *(session, resource, page)
                    ) 
                    for page in range(1, pages+1)
                ]
                for response in await asyncio.gather(*tasks):
                    pass
        
            for task in tasks:
                for data in task.result():
                    result = filter_data(data, resource)
                    if result:
                        resources[resource].update(result)

    return resources


def get_all_resources():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(get_all())

    resources = loop.run_until_complete(future)
    return filter_resources(resources)
    