from crackling.isslOTScoring import isslOTScoring
from crackling.Helpers import *
from crackling.Constants import *
from crackling import ConfigManager

def test_scoringMethod():
    # call the scoring method
    runner([
            '..\\..\\..\\bin\\isslScoreOfftargets.exe',
            'data\\test_genome_offTargets_indexed.issl',
            'data\\test_OTscoring_input.txt',
            '4',
            '75',
            'mit',
            '>',
            'data\\test_OTscoring_output.txt',
        ],
        shell=True,
        check=True
    )

    with open('data\\test_OTscoring_output.txt', 'r') as output:
        result = output.readlines()

    expected = [
        'this'
    ]

    assert expected == result


def test_isslOTScoring():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create result candidate guide dictionary
    result = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
    }

    # Create expected results candidate guide dictionary
    expected = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'mitOfftargetscore'     : CODE_UNTESTED,
            'cfdOfftargetscore'     : CODE_UNTESTED,
            'passedOffTargetScore'  : CODE_UNTESTED
        },
    }

    # Run mm10db
    isslOTScoring(result, cm)
    assert expected == result