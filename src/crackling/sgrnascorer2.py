from crackling.ConfigManager import ConfigManager
from crackling.Helpers import *
from crackling.Constants import *
import joblib

# Define encoding table once
encoding = {
    'A' : '0001',    'C' : '0010',    'T' : '0100',    'G' : '1000',
    'K' : '1100',    'M' : '0011',    'R' : '1001',    'Y' : '0110',
    'S' : '1010',    'W' : '0101',    'B' : '1110',    'V' : '1011',
    'H' : '0111',    'D' : '1101',    'N' : '1111'
}

def sgrnascorer2(candidateGuides: dict, configMngr: ConfigManager):
    # Check if this module needs to be run
    if (configMngr['consensus'].getboolean('sgRNAScorer2')):
        #########################################
        ##         sgRNAScorer 2.0 model       ##
        #########################################
        printer('sgRNAScorer2 - score using model.')
        clfLinear = joblib.load(configMngr['sgrnascorer2']['model'])
        failedCount = 0
        testedCount = 0
        # Run time optimisation
        for target23 in filterCandidateGuides(configMngr, candidateGuides, MODULE_SGRNASCORER2):
            sequence = target23.upper()
            entryList = []
            testedCount += 1
            for x in range(0, 20):
                for y in range(0, 4):
                    entryList.append(int(encoding[sequence[x]][y]))
            # predict based on the entry
            # The following line is not required as the result is not used.
            # prediction = clfLinear.predict([entryList])
            score = clfLinear.decision_function([entryList])[0]
            candidateGuides[target23]['sgrnascorer2score'] = score
            if score < configMngr['sgrnascorer2'].getfloat('score-threshold'):
                candidateGuides[target23]['acceptedBySgRnaScorer'] = CODE_REJECTED
                failedCount += 1
            else:
                candidateGuides[target23]['acceptedBySgRnaScorer'] = CODE_ACCEPTED
        printer(f'\t{failedCount:,} of {testedCount:,} failed here.')