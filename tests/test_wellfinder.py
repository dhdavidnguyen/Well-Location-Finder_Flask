import pytest
from wellfinder import *

path = 'AllWells.csv'
wellname = '41-31R'

def test_wellnav():
    value = wellnav(path, wellname)
    assert value == 'https://www.google.com/maps/dir/?api=1&destination=35.281361,-119.546928'

def test_missingwell():
    value = wellnav(path, 'fakewell')
    assert value == 'https://www.google.com/maps/dir/?api=1&destination=Series([], ),Series([], )'