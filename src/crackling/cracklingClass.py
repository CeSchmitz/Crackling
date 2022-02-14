import csv, os, sys, time
from crackling.ConfigManager import ConfigManager
from crackling.Constants import *
from crackling.Helpers import *
from crackling.inputProcessing import processInput
from crackling.chopchop import chopchop
from crackling.mm10db import mm10db
from crackling.sgrnascorer2 import sgrnascorer2
from crackling.bowtie2 import bowtie2
from crackling.isslOTScoring import isslOTScoring


class Crackling():
    def __init__(self, configMngr: ConfigManager = None):
        self.configMngr = configMngr

    def run(self):
        ###################################
        ##       Setup file logging      ##
        ################################### 
        # Setup file logging
        _stdout = sys.stdout
        _stderr = sys.stderr
        sys.stdout = self.configMngr.getLogMethod()
        sys.stderr = self.configMngr.getErrLogMethod()

        # Record start time
        startTime = time.time()

        ###################################
        ##   Processing the input file   ##
        ###################################
        batchinator = processInput(self.configMngr)


        for candidateGuides in batchinator:
            # Record batch start time
            batchStartTime = time.time()
            printer(f'Processing batch file {(batchinator.currentBatch):,} of {len(batchinator)}')
            printer(f'\tLoaded {len(candidateGuides):,} guides')


            #########################################
            ##              ChopChop               ##
            #########################################
            chopchop(candidateGuides, self.configMngr)


            #########################################
            ##                mm10db               ##
            #########################################
            mm10db(candidateGuides, self.configMngr)


            #########################################
            ##         sgRNAScorer 2.0 model       ##
            #########################################
            sgrnascorer2(candidateGuides, self.configMngr)


            #########################################
            ##      Begin efficacy consensus       ##
            #########################################
            printer('Evaluating efficiency via consensus approach.')
            failedCount = 0
            testedCount = 0
            for target23 in candidateGuides:
                candidateGuides[target23]['consensusCount'] = sum([
                    candidateGuides[target23]['acceptedByMm10db'] == CODE_ACCEPTED,
                    candidateGuides[target23]['acceptedBySgRnaScorer'] == CODE_ACCEPTED,
                    candidateGuides[target23]['passedG20'] == CODE_ACCEPTED,
                ])
                if candidateGuides[target23]['consensusCount'] < self.configMngr['consensus'].getint('n'):
                    failedCount += 1
                testedCount += 1
            printer(f'\t{failedCount:,} of {testedCount:,} failed here.')


            ############################################
            ##         Bowtie2 offtarget scoring      ##
            ############################################
            bowtie2(candidateGuides, self.configMngr)


            #########################################
            ##      Begin off-target scoring       ##
            #########################################
            isslOTScoring(candidateGuides, self.configMngr)


            #########################################
            ##           Begin output              ##
            #########################################
            printer('Writing results to file.')
            # Write guides to file. Include scores etc.
            with open(self.configMngr['output']['file'], 'a+') as fOpen:
                csvWriter = csv.writer(fOpen, delimiter=self.configMngr['output']['delimiter'],
                                quotechar='"',dialect='unix', quoting=csv.QUOTE_MINIMAL)
                for target23 in candidateGuides:
                    output = [candidateGuides[target23][x] for x in DEFAULT_GUIDE_PROPERTIES_ORDER]
                    csvWriter.writerow(output)

            #########################################
            ##              Clean up               ##
            #########################################
            printer('Cleaning auxiliary files')
            for f in [
                self.configMngr['rnafold']['input'],
                self.configMngr['rnafold']['output'],
                self.configMngr['offtargetscore']['input'],
                self.configMngr['offtargetscore']['output'],
                self.configMngr['bowtie2']['input'],
                self.configMngr['bowtie2']['output'],
            ]:
                try:
                    os.remove(f)
                except:
                    pass

            #########################################
            ##               Done                  ##
            #########################################
            printer('Done.')

            printer(f'{len(candidateGuides)} guides evaluated.')

            printer('This batch ran in {} (dd hh:mm:ss) or {} seconds'.format(
                time.strftime('%d %H:%M:%S', time.gmtime((time.time() - batchStartTime))),
                (time.time() - batchStartTime)
            ))

        printer('Total run time (dd hh:mm:ss) or {} seconds'.format(
            time.strftime('%d %H:%M:%S', time.gmtime((time.time() - startTime))),
            (time.time() - startTime)
        ))

        sys.stdout.log.close()
        sys.stderr.log.close()
        sys.stdout = _stdout
        sys.stderr = _stderr

    def validate(self):
        if self.configMngr.isConfigured() == False:
            printer("Please check the format of config file and try again.")
        else: 
            self.valid = True

