from crackling.bowtie2 import bowtie2
from crackling.Helpers import *
from crackling.Constants import *
from crackling import ConfigManager


def test_bowtie2():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create result candidate guide dictionary
    result = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
    }

    # Create expected results candidate guide dictionary
    expected = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'bowtieChr'     : CODE_UNTESTED,
            'bowtieStart'   : CODE_UNTESTED,
            'bowtieEnd'     : CODE_UNTESTED,
            'passedBowtie'  : CODE_UNTESTED
        },
    }

    # Run mm10db
    bowtie2(result, cm)
    assert expected == result