from crackling.bowtie2 import bowtie2
from crackling.Helpers import *
from crackling.Constants import *
from crackling import ConfigManager
import pytest, os

@pytest.fixture
def bowtie2_setup():
    # Setup 
    # (Nothing to setup)
    # NOTE: Everything after yeild is considered teardown as per Pytest documentation. (https://docs.pytest.org/en/7.0.x/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization)
    yield 
    # Teardown
    os.remove('data/output/test-bowtie-input.txt')
    os.remove('data/output/test-bowtie-output.txt')

def test_bowtie2(bowtie2_setup):
    # Setup Config Manager
    cm = ConfigManager('data/unit-testing/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create result candidate guide dictionary
    result = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    expected = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'bowtieChr'     : 'Guide1-different-PAM-1',
            'bowtieStart'   : 1,
            'bowtieEnd'     : 23,
            'passedBowtie'  : CODE_REJECTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'bowtieChr'     : 'Guide2',
            'bowtieStart'   : 1,
            'bowtieEnd'     : 23,
            'passedBowtie'  : CODE_ACCEPTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'bowtieChr'     : 'Guide3',
            'bowtieStart'   : 1,
            'bowtieEnd'     : 23,
            'passedBowtie'  : CODE_REJECTED
        }
    }

    # Run mm10db
    bowtie2(result, cm)
    assert expected == result