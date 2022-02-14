import nose.tools, nose
from  crackling.Constants import *

#######################
## Testing Constants ##
#######################
def test_CODE_ACCEPTED_value():
    nose.tools.eq_(1, CODE_ACCEPTED, f'\nExpected:\t{1}\nActually:\t{CODE_ACCEPTED}')

def test_CODE_REJECTED_value():
    nose.tools.eq_(0, CODE_REJECTED, f'\nExpected:\t{0}\nActually:\t{CODE_REJECTED}')

def test_CODE_AMBIGUOS_value():
    nose.tools.eq_('-', CODE_AMBIGUOUS, f'\nExpected:\t{"-"}\nActually:\t{CODE_AMBIGUOUS}')

def test_CODE_UNTESTED_value():
    nose.tools.eq_('?', CODE_UNTESTED, f'\nExpected:\t{"?"}\nActually:\t{CODE_UNTESTED}')

def test_MODULE_10DB_value():
    nose.tools.eq_('mm10db', MODULE_MM10DB, f'\nExpected:\t{"mm10db"}\nActually:\t{MODULE_MM10DB}')

def test_MODULE_SGRNASCORER2_value():
    nose.tools.eq_('sgrnascorer2', MODULE_SGRNASCORER2, f'\nExpected:\t{"sgrnascorer2"}\nActually:\t{MODULE_SGRNASCORER2}')

def test_MODULE_CHOPCHOP_value():
    nose.tools.eq_('chopchop', MODULE_CHOPCHOP, f'\nExpected:\t{"chopchop"}\nActually:\t{MODULE_CHOPCHOP}')

def test_MODULE_CONSENSUS_value():
    nose.tools.eq_('consensus', MODULE_CONSENSUS, f'\nExpected:\t{"consensus"}\nActually:\t{MODULE_CONSENSUS}')

def test_MODULE_SPECIFICTY_value():
    nose.tools.eq_('specificity', MODULE_SPECIFICITY, f'\nExpected:\t{"specificity"}\nActually:\t{MODULE_SPECIFICITY}')

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
    nose.tools.eq_(expectedResults, DEFAULT_GUIDE_PROPERTIES, f'\nExpected:\t{expectedResults}\nActually:\t{DEFAULT_GUIDE_PROPERTIES}')

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
    nose.tools.eq_(expectedResults, DEFAULT_GUIDE_PROPERTIES_ORDER, f'\nExpected:\t{expectedResults}\nActually:\t{DEFAULT_GUIDE_PROPERTIES_ORDER}')


if __name__ == '__main__':
    nose.run()