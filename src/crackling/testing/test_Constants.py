from  crackling.Constants import *

#######################
## Testing Constants ##
#######################
def test_CODE_ACCEPTED_value():
    assert 1 == CODE_ACCEPTED

def test_CODE_REJECTED_value():
    assert 0 == CODE_REJECTED

def test_CODE_AMBIGUOS_value():
    assert '-' == CODE_AMBIGUOUS

def test_CODE_UNTESTED_value():
    assert '?' == CODE_UNTESTED

def test_MODULE_10DB_value():
    assert 'mm10db' == MODULE_MM10DB

def test_MODULE_SGRNASCORER2_value():
    assert 'sgrnascorer2' == MODULE_SGRNASCORER2

def test_MODULE_CHOPCHOP_value():
    assert 'chopchop' == MODULE_CHOPCHOP

def test_MODULE_CONSENSUS_value():
    assert 'consensus' == MODULE_CONSENSUS

def test_MODULE_SPECIFICTY_value():
    assert 'specificity' == MODULE_SPECIFICITY

def test_DEFAULT_GUIDE_PROPERTIES_value():
    expectedResults = {
    'seq'                       : "",
    'header'                    : "",
    'isUnique'                  : CODE_ACCEPTED,
    'start'                     : CODE_UNTESTED,
    'end'                       : CODE_UNTESTED,
    'strand'                    : CODE_UNTESTED,
    'passedTTTT'                : CODE_UNTESTED,
    'passedATPercent'           : CODE_UNTESTED,
    'passedG20'                 : CODE_UNTESTED,
    'passedSecondaryStructure'  : CODE_UNTESTED,
    'ssL1'                      : CODE_UNTESTED,
    'ssStructure'               : CODE_UNTESTED,
    'ssEnergy'                  : CODE_UNTESTED,
    'acceptedByMm10db'          : CODE_UNTESTED,
    'acceptedBySgRnaScorer'     : CODE_UNTESTED,
    'consensusCount'            : CODE_UNTESTED,
    'passedBowtie'              : CODE_UNTESTED,
    'passedOffTargetScore'      : CODE_UNTESTED,
    'sgrnascorer2score'         : CODE_UNTESTED,
    'AT'                        : CODE_UNTESTED,
    'bowtieChr'                 : CODE_UNTESTED,
    'bowtieStart'               : CODE_UNTESTED,
    'bowtieEnd'                 : CODE_UNTESTED,
    'mitOfftargetscore'         : CODE_UNTESTED,
    'cfdOfftargetscore'         : CODE_UNTESTED,
    'passedAvoidLeadingT'       : CODE_UNTESTED,
    }
    assert expectedResults == DEFAULT_GUIDE_PROPERTIES

def test_DEFAULT_GUIDE_PROPERTIES_ORDER_value():
    expectedResults = [
    'seq',
    'sgrnascorer2score',
    'header',
    'start',
    'end',
    'strand',
    'isUnique',
    'passedG20',
    'passedTTTT',
    'passedATPercent',
    'passedSecondaryStructure',
    'ssL1',
    'ssStructure',
    'ssEnergy',
    'acceptedByMm10db',
    'acceptedBySgRnaScorer',
    'consensusCount',
    'passedBowtie',
    'passedOffTargetScore',
    'AT',
    'bowtieChr',
    'bowtieStart',
    'bowtieEnd',
    'mitOfftargetscore',
    'cfdOfftargetscore',
    'passedAvoidLeadingT',
    ]
    assert expectedResults == DEFAULT_GUIDE_PROPERTIES_ORDER