def test_search():
    import pwaqi

    res = pwaqi.findStationCodesByCity('bangalore', 'demo')

    assert len(res) > 0
    assert 8190 in res


def test_observations():
    import pwaqi

    station = 1437
    res = pwaqi.get_station_observation(station, 'demo')

    assert 'city' in res
    assert station == res['idx']


def test_no_station():
    import pwaqi

    station = 1
    res = pwaqi.get_station_observation(station, 'demo')

    assert res['idx'] == 1437
