from crackling.ConfigManager import ConfigManager
from crackling.Constants import *
from crackling.Helpers import *
from crackling.Paginator import Paginator
import os

def isslOTScoring(candidateGuides: dict, configMngr: ConfigManager):
    if (configMngr['offtargetscore'].getboolean('enabled')):
        #########################################
        ##      Begin off-target scoring       ##
        #########################################
        printer('Beginning off-target scoring.')
        testedCount = 0
        failedCount = 0

        pgLength = configMngr['offtargetscore'].getint('page-length')

        for pgIdx, pageCandidateGuides in Paginator(
            filterCandidateGuides(configMngr, candidateGuides, MODULE_SPECIFICITY),
            pgLength
        ):

            if pgLength > 0:
                printer(f'\tProcessing page {(pgIdx+1)} ({pgLength:,} per page).')

            # prepare the list of candidate guides to score
            guidesInPage = 0
            with open(configMngr['offtargetscore']['input'], 'w') as fTargetsToScore:
                for target23 in pageCandidateGuides:
                    target = target23[0:20]
                    fTargetsToScore.write(target+'\n')
                    testedCount += 1
                    guidesInPage += 1

            if guidesInPage != pgLength:
                printer(f'\t\t{guidesInPage:,} guides in this page.')

            # Convert line endings (Windows)
            if os.name == 'nt':
                runner('dos2unix {}'.format(
                        configMngr['offtargetscore']['input']
                    ),
                    shell=True,
                    check=True
                )

            # call the scoring method
            runner('{} {} {} {} {} {} > {}'.format(
                    configMngr['offtargetscore']['binary'],
                    configMngr['input']['offtarget-sites'],
                    configMngr['offtargetscore']['input'],
                    str(configMngr['offtargetscore']['max-distance']),
                    str(configMngr['offtargetscore']['score-threshold']),
                    str(configMngr['offtargetscore']['method']),
                    configMngr['offtargetscore']['output'],
                ),
                shell=True,
                check=True
            )

            targetsScored = {}
            with open(configMngr['offtargetscore']['output'], 'r') as fTargetsScored:
                for targetScored in [x.split('\t') for x in fTargetsScored.readlines()]:
                    if len(targetScored) == 3:
                        targetsScored[targetScored[0]] = {'MIT': -1.0, 'CFD': -1.0}
                        targetsScored[targetScored[0]]['MIT'] = float(targetScored[1].strip())
                        targetsScored[targetScored[0]]['CFD'] = float(targetScored[2].strip())

            failedCount = 0
            for target23 in pageCandidateGuides:
                if target23[0:20] in targetsScored:
                    score = targetsScored[target23[0:20]]
                    candidateGuides[target23]['mitOfftargetscore'] = score['MIT']
                    candidateGuides[target23]['cfdOfftargetscore'] = score['CFD']
                    scoreThreshold = float(configMngr['offtargetscore']['score-threshold'])
                    scoreMethod = str(configMngr['offtargetscore']['method']).strip().lower()

                    # MIT
                    if scoreMethod == 'mit':
                        if score['MIT'] < scoreThreshold:
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_REJECTED
                            failedCount += 1
                        else:
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_ACCEPTED

                    # CFD
                    elif scoreMethod == 'cfd':
                        if score['CFD'] < scoreThreshold:
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_REJECTED
                            failedCount += 1
                        else:
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_ACCEPTED

                    # AND
                    elif scoreMethod == 'and':
                        if (score['MIT'] < scoreThreshold) and (score['CFD'] < scoreThreshold):
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_REJECTED
                            failedCount += 1
                        else:
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_ACCEPTED

                    # OR
                    elif scoreMethod == 'or':
                        if (score['MIT'] < scoreThreshold) or (score['CFD'] < scoreThreshold):
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_REJECTED
                            failedCount += 1
                        else:
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_ACCEPTED

                    # AVERAGE
                    elif scoreMethod == 'avg':
                        if ((score['MIT'] + score['CFD'])/2) < scoreThreshold:
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_REJECTED
                            failedCount += 1
                        else:
                            candidateGuides[target23]['passedOffTargetScore'] = CODE_ACCEPTED

            printer(f'\t{failedCount:,} of {testedCount:,} failed here.')