import requests
from urllib.parse import unquote
from datetime import datetime

def findStationCodesByCity(cityName):
	r = requests.get("https://wind.waqi.info/nsearch/station/" + cityName)

	if r.status_code == 200:
		return [result["x"] for result in r.json()["results"]]
	else:
		return []

def decoder(todecode):
	decoded = [chr(ord(c)-1) for c in unquote(todecode)]
	return "".join(decoded)

def getJSKey(locationName):
	r = requests.get("http://aqicn.org/city/" + locationName)
	if r.status_code == 200:
		pos = r.text.find("decodeURIComponent")
		todecode = r.text[pos+20:pos+76]
		key = decoder(todecode)
		print("key = {}".format(key))
		return key
	return ""

def getToken(stationCode):
	rToken = requests.get("https://waqi.info/api/token/" + str(stationCode))
	print("token = {}".format(unquote(rToken.json()["rxs"]["obs"][0]["msg"]["token"])))
	return unquote(rToken.json()["rxs"]["obs"][0]["msg"]["token"])

def getUID():
	return  "abcde" + datetime.now().strftime("%s000")

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
