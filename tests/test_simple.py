import os


def test_search():
    import pwaqi

    token = os.environ.get('AQICN_API_TOKEN', 'demo')
    res = pwaqi.findStationCodesByCity('bangalore', token)

    assert len(res) > 0
    assert 8190 in res


def test_invalid_location():
    import pwaqi

    token = os.environ.get('AQICN_API_TOKEN', 'demo')
    res = pwaqi.findStationCodesByCity('INVALID_CITY_NAME', token)

    assert len(res) == 0


def test_observations():
    import pwaqi

    station = 1437
    token = os.environ.get('AQICN_API_TOKEN', 'demo')
    res = pwaqi.get_station_observation(station, token)

    assert 'city' in res
    assert station == res['idx']


def test_no_station():
    import pwaqi

    station = 10000
    token = os.environ.get('AQICN_API_TOKEN', 'demo')
    res = pwaqi.get_station_observation(station, token)

    assert res['idx'] == -1
