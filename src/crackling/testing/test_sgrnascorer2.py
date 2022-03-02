from crackling.sgrnascorer2 import sgrnascorer2
from crackling.Constants import *
from crackling import ConfigManager

##########################
## Testing sgrnaScorer2 ##
##########################s
def test_sgranscorer2_onTestDataset():
    # Setup Config Manager
    cm = ConfigManager('data/unit-testing/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create result candidate guide dictionary
    result = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    expected = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'acceptedBySgRnaScorer' : CODE_REJECTED,
            'sgrnascorer2score'     : -1.8394958342445178
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'acceptedBySgRnaScorer' : CODE_REJECTED,
            'sgrnascorer2score'     : -3.3132386532897384
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'acceptedBySgRnaScorer' : CODE_REJECTED,
            'sgrnascorer2score'     : -0.328729309372379
        }
    }

    # Run sgrnaScorer2
    sgrnascorer2(result, cm)
    assert expected == result