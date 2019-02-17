from decide import lic


def test_lic0_met():
    """LIC 0 should be met when two consecutive points are more than LENGTH1 apart"""
    assert lic.lic_0([[0, 0], [1, 1], [3, 3]], {"length1": 2}) is True


def test_lic0_not_met():
    """LIC 0 should not be met when no consecutive points are more than LENGTH1 apart"""
    assert lic.lic_0([[0, 0], [1, 1], [2, 2]], {"length1": 2}) is False
