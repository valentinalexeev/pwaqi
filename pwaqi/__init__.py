import requests

def findStationCodesByCity(cityName, token):
	r = requests.get('https://api.waqi.info/search/',
		params = {
			'token': token,
			'keyword': cityName
		})

	if r.status_code == 200 and r.json()["status"] == "ok":
		return [result["uid"] for result in r.json()["data"]]
	else:
		return []

def getStationObservation(stationCode, token, locationName='', language = "en"):
	r = requests.get('https://api.waqi.info/api/feed/@%d/obs.%s.json' % (stationCode, language),
		params = {
			'token': token
			})

	if r.status_code == 200:
		obsJson = None
		for res in r.json()["rxs"]["obs"]:
			if "msg" in res:
				obsJson = res["msg"]

		if not obsJson:
			return {}

		def iaqiTranslate(iaqi):
			return {'p': iaqi['p'], 'cur': iaqi['v'][0], 'min': iaqi['v'][1], 'max': iaqi['v'][2]}

		return {
			'city': obsJson.get('city', ''),
			'aqi': obsJson['aqi'],
			'iaqi': [iaqiTranslate(item) for item in obsJson['iaqi']],
			'dominentpol': obsJson.get("dominentpol", ''),
                        'time': obsJson['time']['v']
			}
	else:
		return {}
