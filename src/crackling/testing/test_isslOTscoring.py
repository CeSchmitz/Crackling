from crackling.isslOTScoring import isslOTScoring
from crackling.Helpers import *
from crackling.Constants import *
from crackling import ConfigManager
import pytest, os

@pytest.fixture
def isslScoreOfftargets_setup():
    # Setup
    test_input = [
        'ACTCCTCATGCTGGACATTC\n'
        'ATTCTGGTTCCTAGTATATC\n'
        'GTATATCTGGAGAGTTAAGA\n'
    ]
    with open('input.txt', 'w') as input:
        input.writelines(test_input)
    # NOTE: Everything after yeild is considered teardown as per Pytest documentation. (https://docs.pytest.org/en/7.0.x/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization)
    yield 
    # Teardown
    os.remove('input.txt')
    os.remove('output.txt')

def test_isslScoreOfftargets(isslScoreOfftargets_setup):
    # call the scoring method
    runner('{} {} {} {} {} {} > {}'.format(
            '../../../bin/isslScoreOfftargets',
            'data/test_genome_offTargets_indexed.issl',
            'input.txt',
            '4',
            '75',
            'mit',
            'output.txt',
        ),
        shell=True,
        check=True
    )

    with open('output.txt', 'r') as output:
        result = output.readlines()

    expected = [
        'ACTCCTCATGCTGGACATTC\t100.000000\t-1\n',
        'ATTCTGGTTCCTAGTATATC\t62.186716\t-1\n',
        'GTATATCTGGAGAGTTAAGA\t100.000000\t-1\n'
    ]

    assert expected == result


def test_isslOTScoring_mitScoring():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Set scoring method
    cm['offtargetscore']['method'] = 'mit'
    # Create result candidate guide dictionary
    result = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    expected = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : 100.000000,
            'cfdOfftargetscore'     : -1.0,
            'passedOffTargetScore'  : CODE_ACCEPTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : 62.186716,
            'cfdOfftargetscore'     : -1.0,
            'passedOffTargetScore'  : CODE_REJECTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : 100.000000,
            'cfdOfftargetscore'     : -1.0,
            'passedOffTargetScore'  : CODE_ACCEPTED
        }
    }

    # Run mm10db
    isslOTScoring(result, cm)
    assert expected == result

def test_isslOTScoring_cfdScoring():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Set scoring method
    cm['offtargetscore']['method'] = 'cfd'
    # Create result candidate guide dictionary
    result = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    expected = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : -1.0,
            'cfdOfftargetscore'     : 100.00,
            'passedOffTargetScore'  : CODE_ACCEPTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : -1.0,
            'cfdOfftargetscore'     : 99.247117,
            'passedOffTargetScore'  : CODE_ACCEPTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : -1.0,
            'cfdOfftargetscore'     : 98.039216,
            'passedOffTargetScore'  : CODE_ACCEPTED
        }
    }

    # Run mm10db
    isslOTScoring(result, cm)
    assert expected == result

def test_isslOTScoring_andScoring():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Set scoring method
    cm['offtargetscore']['method'] = 'and'
    # Create result candidate guide dictionary
    result = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    # Create expected results candidate guide dictionary
    expected = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : 100.000000,
            'cfdOfftargetscore'     : 100.00,
            'passedOffTargetScore'  : CODE_ACCEPTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : 60.962237,
            'cfdOfftargetscore'     : 99.247117,
            'passedOffTargetScore'  : CODE_ACCEPTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : 100.000000,
            'cfdOfftargetscore'     : 98.039216,
            'passedOffTargetScore'  : CODE_ACCEPTED
        }
    }

    # Run mm10db
    isslOTScoring(result, cm)
    assert expected == result

def test_isslOTScoring_orScoring():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Set scoring method
    cm['offtargetscore']['method'] = 'or'
    # Create result candidate guide dictionary
    result = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    expected = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : 100.000000,
            'cfdOfftargetscore'     : 100.00,
            'passedOffTargetScore'  : CODE_ACCEPTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : 62.186716,
            'cfdOfftargetscore'     : 99.301702,
            'passedOffTargetScore'  : CODE_REJECTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : 100.000000,
            'cfdOfftargetscore'     : 98.039216,
            'passedOffTargetScore'  : CODE_ACCEPTED
        }
    }

    # Run mm10db
    isslOTScoring(result, cm)
    assert expected == result

def test_isslOTScoring_avgScoring():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Set scoring method
    cm['offtargetscore']['method'] = 'avg'
    # Create result candidate guide dictionary
    result = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    expected = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'mitOfftargetscore'     : 100.000000,
            'cfdOfftargetscore'     : 100.00,
            'passedOffTargetScore'  : CODE_ACCEPTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'mitOfftargetscore'     : 60.962237,
            'cfdOfftargetscore'     : 99.247117,
            'passedOffTargetScore'  : CODE_ACCEPTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'mitOfftargetscore'     : 100.000000,
            'cfdOfftargetscore'     : 98.039216,
            'passedOffTargetScore'  : CODE_ACCEPTED
        }
    }

    # Run mm10db
    isslOTScoring(result, cm)
    assert expected == result