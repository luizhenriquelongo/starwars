from utils import (
    order_by_height,
    order_by_mass,
    order_by_gender,
    order_by_name
)

PAGES = {
    'people': 9,
    'planets': 6,
    'films': 1,
    'vehicles': 4,
    'starships': 4
}

BASE_URL = 'https://swapi.dev/api/'

RESOURCES = ['people', 'films', 'starships', 'planets', 'vehicles']

RESOURCES_FILTER = {
    'planets': 'residents',
    'films': 'characters',
    'vehicles': 'pilots',
    'starships': 'pilots'
}

ORDER_FUNCITIONS = {
    'mass': order_by_mass,
    'height': order_by_height,
    'name': order_by_name,
    'gender': order_by_gender,
}
