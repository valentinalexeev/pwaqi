import requests

def findStationCodesByCity(cityName):
	r = requests.get("https://wind.waqi.info/nsearch/station/" + cityName)

	if r.status_code == 200:
		return [result["x"] for result in r.json()["results"]]
	else:
		return []

def getStationObservation(stationCode, language = "en"):
	r = requests.get("https://waqi.info/api/feed/@" + str(stationCode) + "/obs." + language + ".json")

	if r.status_code == 200:
		obsJson = r.json()["rxs"]["obs"][0]["msg"]

		def iaqiTranslate(iaqi):
			return {'p': iaqi['p'], 'cur': iaqi['v'][0], 'min': iaqi['v'][1], 'max': iaqi['v'][2]}

		return {
			'city': obsJson.get('city', ''),
			'aqi': obsJson['aqi'],
			'iaqi': [iaqiTranslate(item) for item in obsJson['iaqi']],
			'dominentpol': obsJson.get("dominentpol", '')
			}
	else:
		return {}
