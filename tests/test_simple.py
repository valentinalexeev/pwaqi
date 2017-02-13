def test_search():
    import pwaqi

    res = pwaqi.findStationCodesByCity('bangalore', 'demo')

    assert len(res) > 0
    assert 8190 in res


def test_observations():
    import pwaqi

    station = 8190
    res = pwaqi.getStationObservation(station, 'demo')

    assert 'city' in res
    assert station == res['city']['idx']
