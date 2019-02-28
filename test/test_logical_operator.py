import pytest

from decide import decide


def test_logical_connector_unknown():
    """Allowed values of string should be ANDD, ORR or NOT_USED"""
    with pytest.raises(ValueError):
        decide.LogicalConnector.create_from_string("SOME_STRING")


@pytest.mark.parametrize("string", [("ANDD"), ("ORR"), ("NOT_USED")])
def test_logical_connector_create(string):
    """
    Test that the expected connector is created
    """
    connector = decide.LogicalConnector.create_from_string(string)
    assert str(connector) == string


@pytest.mark.parametrize(
    "string, op1, op2, expected",
    [
        ("ANDD", True, True, True),
        ("ANDD", True, False, False),
        ("ANDD", False, False, False),
        ("ORR", True, True, True),
        ("ORR", True, False, True),
        ("ORR", False, False, False),
        ("NOT_USED", False, False, True),
    ],
)
def test_logical_connector_apply(string, op1, op2, expected):
    """
    Test that applying the connectors yields the expected results
    """
    connector = decide.LogicalConnector.create_from_string(string)
    assert connector.apply(op1, op2) == expected
