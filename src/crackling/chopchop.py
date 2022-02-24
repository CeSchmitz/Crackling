
from crackling.ConfigManager import ConfigManager
from crackling.Constants import *
from crackling.Helpers import *

def chopchop(candidateGuides: dict, configMngr: ConfigManager):
    # Check if this module needs to be run
    if (configMngr['consensus'].getboolean('CHOPCHOP')):
        #########################################
        ##              ChopChop               ##
        #########################################
        printer('CHOPCHOP - remove those without G in position 20.')
        failedCount = 0
        testedCount = 0
        # Run time optimisation
        for target23 in filterCandidateGuides(configMngr, candidateGuides, MODULE_CHOPCHOP):
            if G20(target23):
                candidateGuides[target23]['passedG20'] = CODE_ACCEPTED
            else:
                candidateGuides[target23]['passedG20'] = CODE_REJECTED
                failedCount += 1
            testedCount += 1
        printer(f'\t{failedCount:,} of {testedCount:,} failed here.')


def G20(candidateGuide: str) -> bool:
    # Type checking
    if (type(candidateGuide) != str):
        raise TypeError('Incorrect input type')
    elif (len(candidateGuide) != 23):
        raise ValueError('Incorrect input length')
    return candidateGuide[19] == 'G'