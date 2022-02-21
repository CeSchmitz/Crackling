from subprocess import run
from datetime import datetime
from crackling.ConfigManager import ConfigManager
from crackling.Constants import *

__all__ = ['rc', 'printer','runner', 'filterCandidateGuides']

# Define translation tables once
complements = str.maketrans('acgtrymkbdhvACGTRYMKBDHV', 'tgcayrkmvhdbTGCAYRKMVHDB')

# Function that returns the reverse-complement of a given sequence
def rc(dna: str) -> str:
    rcseq = dna.translate(complements)[::-1]
    return rcseq


# Function that formats provided text with time stamp
def printer(stringFormat: str) -> None:
    print('>>> {}:\t{}\n'.format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"),
        stringFormat
    ))


# Function that runs given external call and records start and finish times using printer
def runner(*args, **kwargs) -> None:
    printer(f"| Calling: {args}")
    run(*args, **kwargs)
    printer(f"| Finished")


def filterCandidateGuides(configMngr: ConfigManager, candidateGuides: dict, module: str):
    optimisation = configMngr['general']['optimisation']
    consensusN = configMngr['consensus'].getint('n')

    for target23 in candidateGuides:

        if optimisation == 'ultralow':
            pass # Pass will short circuit the if statements and yeild target

        elif optimisation == 'low':
            # Never assess guides that appear twice
            if (candidateGuides[target23]['isUnique'] == CODE_REJECTED):
                continue # Continue will short circuit the for loop statements and process the next entry       

        elif optimisation == 'medium':
            # Never assess guides that appear twice
            if (candidateGuides[target23]['isUnique'] == CODE_REJECTED):
                continue
            # For mm10db:
            if (module == MODULE_MM10DB):
                # if any of the mm10db tests have failed, then fail them all
                if (CODE_REJECTED in [
                    candidateGuides[target23]['passedAvoidLeadingT'],
                    candidateGuides[target23]['passedATPercent'],
                    candidateGuides[target23]['passedTTTT'],
                    candidateGuides[target23]['passedSecondaryStructure'],
                    candidateGuides[target23]['acceptedByMm10db'],
                ]):
                    continue
            # For CHOPCHOP:
            # Always assess, unless the guide is seen multiple times

            # For sgRNAScorer2:
            # Always assess, unless the guide is seen multiple times

            # For specificity:
            if (module == MODULE_SPECIFICITY):
                # don't assess if they failed consensus
                if (int(candidateGuides[target23]['consensusCount']) < consensusN):
                    continue
                # don't assess if they failed Bowtie
                if (candidateGuides[target23]['passedBowtie'] == CODE_REJECTED):
                    continue

        elif optimisation == 'high':
            # Never assess guides that appear twice
            if (candidateGuides[target23]['isUnique'] == CODE_REJECTED):
                continue
            # For efficiency
            if module in [MODULE_CHOPCHOP, MODULE_MM10DB, MODULE_SGRNASCORER2]:

                # `consensusCount` cannot be used yet as it may not have been
                # calculated. instead, calculate it on-the-go.
                countAlreadyAccepted = sum([
                    candidateGuides[target23]['acceptedByMm10db'] == CODE_ACCEPTED,
                    candidateGuides[target23]['passedG20'] == CODE_ACCEPTED,
                    candidateGuides[target23]['acceptedBySgRnaScorer'] == CODE_ACCEPTED,
                ])

                countAlreadyAssessed = sum([
                    candidateGuides[target23]['acceptedByMm10db'] in [CODE_ACCEPTED, CODE_REJECTED],
                    candidateGuides[target23]['passedG20'] in [CODE_ACCEPTED, CODE_REJECTED],
                    candidateGuides[target23]['acceptedBySgRnaScorer'] in [CODE_ACCEPTED, CODE_REJECTED],
                ])

                countToolsInConsensus = sum([
                    configMngr['consensus'].getboolean('mm10db'),
                    configMngr['consensus'].getboolean('chopchop'),
                    configMngr['consensus'].getboolean('sgRNAScorer2'),
                ])

                # Do not assess if passed consensus already
                if countAlreadyAccepted >= consensusN:
                    continue
                # Do not assess if there are not enough remaining tests to pass consensus
                #   i.e. if the number of remaining tests is less than what is needed to pass then do not assess
                if countToolsInConsensus - countAlreadyAssessed < consensusN - countAlreadyAccepted:
                    continue
                # For mm10db:
                if module == MODULE_MM10DB:
                    # if any of the mm10db tests have failed, then fail them all
                    if (CODE_REJECTED in [
                        candidateGuides[target23]['passedAvoidLeadingT'],
                        candidateGuides[target23]['passedATPercent'],
                        candidateGuides[target23]['passedTTTT'],
                        candidateGuides[target23]['passedSecondaryStructure'],
                        candidateGuides[target23]['acceptedByMm10db'],
                    ]):
                        continue
            # For specificity:
            if (module == MODULE_SPECIFICITY):
                # don't assess if they failed consensus
                if (int(candidateGuides[target23]['consensusCount']) < consensusN):
                    continue
                # don't assess if they failed Bowtie
                if (candidateGuides[target23]['passedBowtie'] == CODE_REJECTED):
                    continue
        
        # Given none of the failure conditions have been met, yeild guide
        yield target23