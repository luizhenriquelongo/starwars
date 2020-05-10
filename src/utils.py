from operator import itemgetter


def filter_people(data):
    person = {
        'name': data.get('name'),
        'height': data.get('height'),
        'mass': data.get('mass').replace(',', ''),
        'gender': data.get('gender'),
        'films': data.get('films'),
        'starships': data.get('starships'),
        'vehicles': data.get('vehicles'),
        'homeworld': data.get('homeworld'),
    }

    return {
        data.get('url'): person
    }


def filter_films(data):
    title = f"Episode {data.get('episode_id')}: {data.get('title')}"
    return {
        data.get('url'): {
            'title': title,
            'characters': data.get('characters')
        } 
    }


def string_to_float(text):
    try:
        int(text)
    except ValueError:
        try:
            float(text)
        except ValueError:
            return 0
        else:
            return float(text)
    
    else:
        return int(text)


def calculate_score(hyperdrive_rating, cost_in_credits):
    hr = string_to_float(hyperdrive_rating)
    cc = string_to_float(cost_in_credits)

    if cc == 0:
        return 0
    
    return hr / cc


def filter_starships(data):
    score = calculate_score(data.get('hyperdrive_rating'), data.get('cost_in_credits'))
    return {
        data.get('url'): {
            'name': data.get('name'),
            'model': data.get('model'),
            'manufacturer': data.get('manufacturer'),
            'length': data.get('length').replace(',', '') if isinstance(data.get('length'), str) else data.get('length'),
            'passengers': data.get('passengers').replace(',', '') if isinstance(data.get('passengers'), str) else data.get('passengers'),
            'cargo_capacity': data.get('cargo_capacity').replace(',', '') if isinstance(data.get('cargo_capacity'), str) else data.get('cargo_capacity'),
            'starship_class': data.get('starship_class'),
            'pilots': data.get('pilots'),
            'score': score
        } 
    }


def filter_planets(data):
    return {
        data.get('url'): {
            'name': data.get('name'),
            'residents': data.get('residents'),
        }
    }


def filter_vehicles(data):
    return {
        data.get('url'): {
            'name': data.get('name'),
            'pilots': data.get('pilots')
        } 
    }


def filter_data(data, resource):
    QUERYSET = {
        'people': filter_people,
        'films': filter_films,
        'starships': filter_starships,
        'planets': filter_planets,
        'vehicles': filter_vehicles,
    }
    return QUERYSET[resource](data)


def order_by_mass(dic):
    try:
        int(dic.get('mass'))
    except ValueError:
        try:
            float(dic.get('mass'))
        except ValueError:
            return 0
        else:
            return float(dic.get('mass'))
    
    else:
        return int(dic.get('mass'))


def order_by_height(dic):
    try:
        int(dic.get('height'))
    except ValueError:
        try:
            float(dic.get('height'))
        except ValueError:
            return 0
        else:
            return float(dic.get('height'))
    
    else:
        return int(dic.get('height'))


def order_by_name(dic):
    return itemgetter('name')(dic)


def order_by_gender(dic):
    return itemgetter('gender')(dic)


def filter_resources(resources):
    people = resources['people']
    
    for url, value in people.items():

        named_films = []
        for film in value.get('films', []):
            film_name = resources['films'].get(film, {}).get('title')
            if film_name:
                named_films.append(film_name)
        people[url]['films'] = ', '.join(named_films)

        named_starships = []
        for starship in value.get('starships', []):
            starship_name = resources['starships'].get(starship, {}).get('name')
            if starship_name:
                named_starships.append(starship_name)
        people[url]['starships'] = ', '.join(named_starships)

        named_vehicles = []
        for vehicle in value.get('vehicles', []):
            vehicle_name = resources['vehicles'].get(vehicle, {}).get('name')
            if vehicle_name:
                named_vehicles.append(vehicle_name)
        people[url]['vehicles'] = ', '.join(named_vehicles)

        people[url]['homeworld'] = resources['planets'].get(value.get('homeworld'), {}).get('name')

    resources['people'] = people
    
    return resources
