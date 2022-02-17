from crackling.sgrnascorer2 import sgrnascorer2
from crackling.Constants import *
from crackling import ConfigManager

##########################
## Testing sgrnaScorer2 ##
##########################s
def test_sgranscorer2_onTestDataset():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create result candidate guide dictionary
    result = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
    }

    # Create expected results candidate guide dictionary
    expected = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'acceptedBySgRnaScorer' : CODE_ACCEPTED,
            'sgrnascorer2score'     : 0.6509799174117802
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'acceptedBySgRnaScorer' : CODE_REJECTED,
            'sgrnascorer2score'     : -7.721831867973529
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'acceptedBySgRnaScorer' : CODE_ACCEPTED,
            'sgrnascorer2score'     : 3.5543409089281313
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'acceptedBySgRnaScorer' : CODE_ACCEPTED,
            'sgrnascorer2score'     : 1.221131568891114
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'acceptedBySgRnaScorer' : CODE_REJECTED,
            'sgrnascorer2score'     : -0.18335989838239686
        },
    }

    # Run sgrnaScorer2
    sgrnascorer2(result, cm)
    assert expected == result