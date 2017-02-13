"""
A Python wrapper for AQICN API.

The library can be used to search and retrieve Air Quality Index data.
Please refer to AQICN website to obtain token that must be used for access.
"""
import requests

API_ENDPOINT = 'https://api.waqi.info/'
API_ENDPOINT_SEARCH = API_ENDPOINT + 'search/'
API_ENDPOINT_OBS = API_ENDPOINT + 'api/feed/@%d/obs.%s.json'
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

    if req.station_code == 200 and req.json()["status"] == "ok":
        return parse_observation_response(req.json()["data"])
    return {}


def parse_observation_response(json):
    """Decode AQICN observation response JSON into python object."""
    def iaqi_translate(iaqi):
        """Helper to translate AQI data items."""
        return {
            'p': iaqi['p'],
            'cur': iaqi['v'][0],
            'min': iaqi['v'][1],
            'max': iaqi['v'][2]
            }

    return {
        'city': json.get('city', ''),
        'aqi': json['aqi'],
        'iaqi': [iaqi_translate(item) for item in json['iaqi']],
        'dominentpol': json.get("dominentpol", ''),
        'time': json['time']['v']
    }


def getStationObservation(station_code, token, language="en"):
    """Request station data for a specific station identified by code.

    A language parameter can also be specified to translate location
    information (default: "en")
    """
    req = requests.get(
        API_ENDPOINT_OBS % (station_code, language),
        params={
            'token': token
        })

    if req.status_code == 200:
        obs_json = None
        for res in req.json()["rxs"]["obs"]:
            if "msg" in res:
                obs_json = res["msg"]

        if not obs_json:
            return {}
        return parse_observation_response(obs_json)
    else:
        return {}
