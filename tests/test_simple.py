def test_search():
    import pwaqi

    res = pwaqi.findStationCodesByCity('bangalore', 'demo')

    assert len(res) > 0
    assert 8190 in res['result']


def wrong_token_search():
    import pwaqi

    res = pwaqi.findStationCodesByCity('bangalore', 'asjkfdhasjk')

    assert res['status'] == "error"


def test_observations():
    import pwaqi

    station = 1437
    res = pwaqi.get_station_observation(station, 'demo')

    assert 'city' in res['result']
    assert station == res['result']['idx']


def wrong_token_test_observations():
    import pwaqi

    station = 1437
    res = pwaqi.get_station_observation(station, 'asjkfdhasjk')

    assert res['status'] == "error"


def test_no_station():
    import pwaqi

    station = 1
    res = pwaqi.get_station_observation(station, 'demo')

    assert res['result']['idx'] == 1437
