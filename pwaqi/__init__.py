"""
A Python wrapper for AQICN API.

The library can be used to search and retrieve Air Quality Index data.
Please refer to AQICN website to obtain token that must be used for access.
"""
import logging
import requests

API_ENDPOINT = 'https://api.waqi.info/'
API_ENDPOINT_SEARCH = API_ENDPOINT + 'search/'
API_ENDPOINT_OBS = API_ENDPOINT + 'feed/@%d/'
API_ENDPOINT_GEO = API_ENDPOINT + 'feed/geo:%d;%d/'


def findStationCodesByCity(city_name, token):
    """Lookup AQI database for station codes in a given city."""
    req = requests.get(
        API_ENDPOINT_SEARCH,
        params={
            'token': token,
            'keyword': city_name
        })

    if req.status_code == 200 and req.json()["status"] == "ok":
        return [result["uid"] for result in req.json()["data"]]
    else:
        return []


def get_location_observation(lat, lng, token):
    """Lookup observations by geo coordinates."""
    req = requests.get(
        API_ENDPOINT_GEO % (lat, lng),
        params={
            'token': token
        })

    if req.status_code == 200 and req.json()["status"] == "ok":
        return parse_observation_response(req.json()["data"])
    return {}


def parse_observation_response(json):
    """Decode AQICN observation response JSON into python object."""
    logging.debug(json)

    iaqi = json['iaqi']
    result = {
        'idx': json['idx'],
        'city': json.get('city', ''),
        'aqi': json['aqi'],
        'dominentpol': json.get("dominentpol", ''),
        'time': json['time']['s'],
        'iaqi': [{'p': item, 'v': iaqi[item]['v']} for item in iaqi]
    }

    return result


def get_station_observation(station_code, token):
    """Request station data for a specific station identified by code.

    A language parameter can also be specified to translate location
    information (default: "en")
    """
    req = requests.get(
        API_ENDPOINT_OBS % (station_code),
        params={
            'token': token
        })

    if req.status_code == 200 and req.json()['status'] == "ok":
        return parse_observation_response(req.json()['data'])
    else:
        return {}
