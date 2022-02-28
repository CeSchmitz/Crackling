from crackling.Helpers import *
from crackling import ConfigManager
from crackling.Constants import *
import sys, io, datetime, pytest
from subprocess import CalledProcessError, TimeoutExpired

################
## Testing rc ##
################
def test_rc_onPalindromicSeq():
    result = rc('ACGTACGTACGTACGTACGT')
    expected = 'ACGTACGTACGTACGTACGT'
    assert expected == result

def test_rc_onEmptySeq():
    result = rc('')
    expected = ''
    assert expected == result

def test_rc_onShortSeq():
    result = rc('GACTGG')
    expected = 'CCAGTC'
    assert expected == result

def test_rc_onLongSeq():
    result = rc('GACTGGTTTGTGTCATATTCTTCCTGTGG')
    expected = 'CCACAGGAAGAATATGACACAAACCAGTC'
    assert expected == result

def test_rc_onNumber():
    with pytest.raises(TypeError): 
        rc(123456789)

def test_rc_onArray():
    with pytest.raises(TypeError): 
        rc(['T','A','T','G','T','G','T','G','A','T','A','T','A','C','T','T','G','C','T','G','T','G','G'])

def test_rc_onDictionary():
    with pytest.raises(TypeError): 
        rc({'ATGCATGCATGCATGCATGCAGG':'ATGCATGCATGCATGCATGCAGG'})

#####################
## Testing printer ##
#####################
def test_printer_output():
    # Setting up stdout capture
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    # Generate phrase
    expectedPhrase = 'This is a test phrase: a86a3a279afd9beb2d4e9b202318b58ac65552ddfba5901f24b870153b7b44e6'
    # Run printer function
    printer(expectedPhrase)
    # Reset stdout
    sys.stdout = old_stdout
    # Get caputed stdout value
    result = mystdout.getvalue().strip()
    # Extract phrase
    resultPhrase = result[32:]
    assert expectedPhrase == resultPhrase

def test_printer_timestamp():
    # Setting up stdout capture
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    # Generate time
    expectedDateTime = datetime.datetime.now()
    # Run printer function
    printer('')
    # Reset stdout
    sys.stdout = old_stdout
    # Get caputed stdout value
    result = mystdout.getvalue()
    # Extract date and time
    testDate = list(map(int, result[4:14].split("-")))
    testTime = list(map(int, result[15:30].split(":")))
    resultDateTime = datetime.datetime(
        testDate[0], testDate[1], testDate[2],
        testTime[0], testTime[1], testTime[2], testTime[3]
        )
    assert (resultDateTime - expectedDateTime).total_seconds() < 1e-03


####################
## Testing runner ##
####################
def test_runner_output():
    # Setting up stdout capture
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    # Generate expected result
    expected = [
        "| Calling: ('exit 0',)",
        '',
        '| Finished',
        '',
        ''
    ]
    # Run runner function
    runner('exit 0', shell=True)
    # Reset stdout
    sys.stdout = old_stdout
    # Get caputed stdout value
    result = mystdout.getvalue().split('\n')
    # Strip time stamps
    result[0] = result[0][32:]
    result[2] = result[2][32:]
    assert expected == result

def test_runner_errorChecking():
    with pytest.raises(CalledProcessError):
        # Should raise exception
        runner('exit 1', shell=True, check=True)

def test_runner_timeout():
    with pytest.raises(TimeoutExpired): 
        # Should raise exception
        runner('sleep 2', shell=True, check=True, timeout=1)


###################################
## Testing filterCandidateGuides ##
###################################
def test_filterCandidateGuides_onChopchopUltralow():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_REJECTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        },
        'Guide3': {
            'isUnique'                  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_CHOPCHOP)]

    expected = ['Guide1', 'Guide2', 'Guide3']

    assert expected == result

def test_filterCandidateGuides_onChopchopLow():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'low'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_REJECTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        },
        'Guide3': {
            'isUnique'                  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_CHOPCHOP)]

    expected = ['Guide1', 'Guide2']

    assert expected == result

def test_filterCandidateGuides_onChopchopMedium():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'medium'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_REJECTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        },
        'Guide3': {
            'isUnique'                  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_CHOPCHOP)]

    expected = ['Guide1', 'Guide2']

    assert expected == result

def test_filterCandidateGuides_onChopchopHigh():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'high'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_REJECTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        },
        'Guide3': {
            'isUnique'                  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_UNTESTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_CHOPCHOP)]

    expected = ['Guide1']

    assert expected == result

def test_filterCandidateGuides_onMM10dbUltralow():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_ACCEPTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_REJECTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        },
        'Guide3': {
            'isUnique'                  : CODE_REJECTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_MM10DB)]

    expected = ['Guide1', 'Guide2', 'Guide3']

    assert expected == result

def test_filterCandidateGuides_onMM10dbLow():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'low'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_ACCEPTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_REJECTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        },
        'Guide3': {
            'isUnique'                  : CODE_REJECTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_MM10DB)]

    expected = ['Guide1', 'Guide2']

    assert expected == result

def test_filterCandidateGuides_onMM10dbMedium():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'medium'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_ACCEPTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_REJECTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        },
        'Guide3': {
            'isUnique'                  : CODE_REJECTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_MM10DB)]

    expected = ['Guide2']

    assert expected == result

def test_filterCandidateGuides_onMM10dbHigh():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'high'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_ACCEPTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_REJECTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        },
        'Guide3': {
            'isUnique'                  : CODE_REJECTED,
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'passedTTTT'                : CODE_ACCEPTED,
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_UNTESTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_MM10DB)]

    expected = []

    assert expected == result

def test_filterCandidateGuides_onSgrnaScorer2Ultralow():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        },
        'Guide3': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_REJECTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_SGRNASCORER2)]

    expected = ['Guide1', 'Guide2', 'Guide3']

    assert expected == result

def test_filterCandidateGuides_onSgrnaScorer2Low():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'low'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        },
        'Guide3': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_REJECTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_SGRNASCORER2)]

    expected = ['Guide2', 'Guide3']

    assert expected == result

def test_filterCandidateGuides_onSgrnaScorer2Medium():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'medium'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        },
        'Guide3': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_REJECTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_SGRNASCORER2)]

    expected = ['Guide2', 'Guide3']

    assert expected == result

def test_filterCandidateGuides_onSgrnaScorer2High():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'high'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'                  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        },
        'Guide2': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_ACCEPTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        },
        'Guide3': {
            'isUnique'                  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED,
            'passedG20'                 : CODE_REJECTED,
            'acceptedBySgRnaScorer'     : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_SGRNASCORER2)]

    expected = ['Guide3']

    assert expected == result

def test_filterCandidateGuides_onSpecificityUltralow():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 3,
            'passedBowtie'      : CODE_ACCEPTED
        },
        'Guide2': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 3,
            'passedBowtie'      : CODE_REJECTED
        },
        'Guide3': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 1,
            'passedBowtie'      : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_SPECIFICITY)]

    expected = ['Guide1', 'Guide2', 'Guide3']

    assert expected == result

def test_filterCandidateGuides_onSpecificityLow():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'low'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 3,
            'passedBowtie'      : CODE_ACCEPTED
        },
        'Guide2': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 3,
            'passedBowtie'      : CODE_REJECTED
        },
        'Guide3': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 1,
            'passedBowtie'      : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_SPECIFICITY)]

    expected = ['Guide1', 'Guide2', 'Guide3']

    assert expected == result

def test_filterCandidateGuides_onSpecificityMedium():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'medium'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 3,
            'passedBowtie'      : CODE_ACCEPTED
        },
        'Guide2': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 3,
            'passedBowtie'      : CODE_REJECTED
        },
        'Guide3': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 1,
            'passedBowtie'      : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_SPECIFICITY)]

    expected = ['Guide1']

    assert expected == result

def test_filterCandidateGuides_onSpecificityHigh():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'high'
    # Create test candidate guide dictionary
    testCandidateGuides = {
        'Guide1': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 3,
            'passedBowtie'      : CODE_ACCEPTED
        },
        'Guide2': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 3,
            'passedBowtie'      : CODE_REJECTED
        },
        'Guide3': {
            'isUnique'          : CODE_ACCEPTED,
            'consensusCount'    : 1,
            'passedBowtie'      : CODE_ACCEPTED
        }
    }

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_SPECIFICITY)]

    expected = ['Guide1']

    assert expected == result

def test_filterCandidateGuides_onEmptyDictionary_CandidateGuides():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    testCandidateGuides = {}

    # Create expected results candidate guide dictionary
    result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_SPECIFICITY)]

    expected = []

    assert expected == result

def test_filterCandidateGuides_onNumber_CandidateGuides():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    testCandidateGuides = 1234567890

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_CHOPCHOP)]

def test_filterCandidateGuides_onArray_CandidateGuides():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    testCandidateGuides = ['T','A','T','G','T','G','T','G','A','T','A','T','A','C','T','T','G','C','T','G','T','G','G']

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_CHOPCHOP)]

def test_filterCandidateGuides_onString_CandidateGuides():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    testCandidateGuides = 'ATGCATGCATGCATGCATGCAGG'

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, MODULE_CHOPCHOP)]

def test_filterCandidateGuides_onInvalidModule():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    testCandidateGuides = {}

    with pytest.raises(ValueError):
        result = [guide for guide in filterCandidateGuides(cm, testCandidateGuides, 'invalidmodule')]

def test_filterCandidateGuides_onEmptyDictionary_Module():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    module = {}

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, {}, module)]

def test_filterCandidateGuides_onNumber_Module():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    module = 1234567890

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, {}, module)]

def test_filterCandidateGuides_onArray_Module():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    module = ['T','A','T','G','T','G','T','G','A','T','A','T','A','C','T','T','G','C','T','G','T','G','G']

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, {}, module)]

def test_filterCandidateGuides_onString_Module():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create test candidate guide dictionary
    module = 'ATGCATGCATGCATGCATGCAGG'

    with pytest.raises(ValueError):
        result = [guide for guide in filterCandidateGuides(cm, {}, module)]

def test_filterCandidateGuides_onEmptyDictionary_ConfigManager():
    cm = {}

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, {}, MODULE_CHOPCHOP)]

def test_filterCandidateGuides_onNumber_Module():
    cm = 1234567890

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, {}, MODULE_CHOPCHOP)]

def test_filterCandidateGuides_onArray_Module():
    cm = ['T','A','T','G','T','G','T','G','A','T','A','T','A','C','T','T','G','C','T','G','T','G','G']

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, {}, MODULE_CHOPCHOP)]

def test_filterCandidateGuides_onString_Module():
    cm = 'ATGCATGCATGCATGCATGCAGG'

    with pytest.raises(TypeError):
        result = [guide for guide in filterCandidateGuides(cm, {}, MODULE_CHOPCHOP)]