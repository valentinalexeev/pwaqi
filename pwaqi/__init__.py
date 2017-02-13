"""
A Python wrapper for AQICN API.

The library can be used to search and retrieve Air Quality Index data.
Please refer to AQICN website to obtain token that must be used for access.
"""
import requests

API_ENDPOINT_SEARCH = 'https://api.waqi.info/search/'
API_ENDPOINT_OBS = 'https://api.waqi.info/api/feed/@%d/obs.%s.json'


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

        def iaqi_translate(iaqi):
            """Helper to translate AQI data items."""
            return {
                'p': iaqi['p'],
                'cur': iaqi['v'][0],
                'min': iaqi['v'][1],
                'max': iaqi['v'][2]
                }

        return {
            'city': obs_json.get('city', ''),
            'aqi': obs_json['aqi'],
            'iaqi': [iaqi_translate(item) for item in obs_json['iaqi']],
            'dominentpol': obs_json.get("dominentpol", ''),
            'time': obs_json['time']['v']
        }
    else:
        return {}
