from crackling.ConfigManager import ConfigManager
from crackling.Helpers import *
from crackling.Constants import *
from crackling.Paginator import Paginator
import os, re, ast

def mm10db(candidateGuides: dict, configMngr: ConfigManager):
    # Check if this module needs to be run
    if (configMngr['consensus'].getboolean('mm10db')):
        ############################################
        ##     Removing targets with leading T    ##
        ############################################
        printer('mm10db - remove all targets with a leading T (+) or trailing A (-).')
        failedCount = 0
        testedCount = 0
        # Run time optimisation
        for target23 in filterCandidateGuides(configMngr, candidateGuides, MODULE_MM10DB):
            if leadingT(target23):
                candidateGuides[target23]['passedAvoidLeadingT'] = CODE_REJECTED
                failedCount += 1
            else:
                candidateGuides[target23]['passedAvoidLeadingT'] = CODE_ACCEPTED
            testedCount += 1
        printer(f'\t{failedCount:,} of {testedCount:,} failed here.')


        #########################################
        ##    AT% ideally is between 20-65%    ##
        #########################################
        printer('mm10db - remove based on AT percent.')
        failedCount = 0
        testedCount = 0
        # Run time optimisation
        for target23 in filterCandidateGuides(configMngr, candidateGuides, MODULE_MM10DB):
            AT = AT_percentage(target23[0:20])
            if AT < 20 or AT > 65:
                candidateGuides[target23]['passedATPercent'] = CODE_REJECTED
                failedCount += 1
            else:
                candidateGuides[target23]['passedATPercent'] = CODE_ACCEPTED
            candidateGuides[target23]['AT'] = AT
            testedCount += 1
        printer(f'\t{failedCount:,} of {testedCount:,} failed here.')


        ############################################
        ##   Removing targets that contain TTTT   ##
        ############################################
        printer('mm10db - remove all targets that contain TTTT.')
        failedCount = 0
        testedCount = 0
        # Run time optimisation
        for target23 in filterCandidateGuides(configMngr, candidateGuides, MODULE_MM10DB):
            if polyT(target23):
                candidateGuides[target23]['passedTTTT'] = CODE_REJECTED
                failedCount += 1
            else:
                candidateGuides[target23]['passedTTTT'] = CODE_ACCEPTED
            testedCount += 1
        printer(f'\t{failedCount:,} of {testedCount:,} failed here.')


        ##########################################
        ##   Calculating secondary structures   ##
        ##########################################
        printer('mm10db - check secondary structure.')
        guide = 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU'
        pattern_RNAstructure = r'.{28}\({4}\.{4}\){4}\.{3}\){4}.{21}\({4}\.{4}\){4}\({7}\.{3}\){7}\.{3}\s\((.+)\)'
        pattern_RNAenergy = r'\s\((.+)\)'
        testedCount = 0
        failedCount = 0
        errorCount = 0
        notFoundCount = 0
        # RNAFold is memory intensive for very large datasets.
        # We will paginate in order not to overflow memory.
        pgLength = configMngr['rnafold'].getint('page-length')
        # Run time optimisation
        for pgIdx, pageCandidateGuides in Paginator(
            filterCandidateGuides(configMngr, candidateGuides, MODULE_MM10DB),
            pgLength
        ):
            if pgLength > 0:
                printer(f'\tProcessing page {(pgIdx+1)} ({pgLength:,} per page).')

            printer('\t\tConstructing the RNAfold input file.')
            guidesInPage = 0
            with open(configMngr['rnafold']['input'], 'w+') as fRnaInput:
                for target23 in pageCandidateGuides:
                    fRnaInput.write(f'G{target23[1:20]}{guide}\n')
                    guidesInPage += 1
            printer(f'\t\t{guidesInPage:,} guides in this page.')

            runner('{} --noPS -j{} -i {} -o'.format(
                    configMngr['rnafold']['binary'],
                    configMngr['rnafold']['threads'],
                    configMngr['rnafold']['input']
                ),
                shell=True,
                check=True
            )

            # Change implemented to stop RNAfold hanging on windows. Should be revisited later
            os.replace('RNAfold_output.fold' ,configMngr['rnafold']['output'])
            printer('\t\tStarting to process the RNAfold results.')
            RNAstructures = {}
            with open(configMngr['rnafold']['output'], 'r') as fRnaOutput:
                i = 0
                L1, L2, target = None, None, None
                for line in fRnaOutput:
                    if i % 2 == 0:
                        # 0th, 2nd, 4th, etc.
                        L1 = line.rstrip()
                        target = L1[0:20]
                    else:
                        # 1st, 3rd, 5th, etc.
                        L2 = line.rstrip()
                        RNAstructures[transToDNA(target[1:20])] = [
                            L1, L2, target
                        ]
                    i += 1

            for target23 in pageCandidateGuides:
                key = target23[1:20]
                if key not in RNAstructures:
                    print(f'Could not find: {target23[0:20]}')
                    notFoundCount += 1
                    continue
                else:
                    L1 = RNAstructures[key][0]
                    L2 = RNAstructures[key][1]
                    target = RNAstructures[key][2]
                structure = L2.split(' ')[0]
                energy = L2.split(' ')[1][1:-1]
                candidateGuides[target23]['ssL1'] = L1
                candidateGuides[target23]['ssStructure'] = structure
                candidateGuides[target23]['ssEnergy'] = energy
                if transToDNA(target) != target23[0:20] and transToDNA('C'+target[1:]) != target23[0:20] and transToDNA('A'+target[1:]) != target23[0:20]:
                    candidateGuides[target23]['passedSecondaryStructure'] = CODE_ERROR
                    errorCount += 1
                    continue
                match_structure = re.search(pattern_RNAstructure, L2)
                if match_structure:
                    energy = ast.literal_eval(match_structure.group(1))
                    if energy < float(configMngr['rnafold']['low_energy_threshold']):
                        candidateGuides[transToDNA(target23)]['passedSecondaryStructure'] = CODE_REJECTED
                        failedCount += 1
                    else:
                        candidateGuides[target23]['passedSecondaryStructure'] = CODE_ACCEPTED
                else:
                    match_energy = re.search(pattern_RNAenergy, L2)
                    if match_energy:
                        energy = ast.literal_eval(match_energy.group(1))
                        if energy <= float(configMngr['rnafold']['high_energy_threshold']):
                            candidateGuides[transToDNA(target23)]['passedSecondaryStructure'] = CODE_REJECTED
                            failedCount += 1
                        else:
                            candidateGuides[target23]['passedSecondaryStructure'] = CODE_ACCEPTED
                testedCount += 1

        printer(f'\t{failedCount:,} of {testedCount:,} failed here.')
        if errorCount > 0:
            printer(f'\t{errorCount} of {testedCount} erred here.')
        if notFoundCount > 0:
            printer(f'\t{notFoundCount} of {testedCount} not found in RNAfold output.')

        #########################################
        ##         Calc mm10db result          ##
        #########################################
        printer('Calculating mm10db final result.')
        acceptedCount = 0
        failedCount = 0
        for target23 in candidateGuides:
            if not all([
                candidateGuides[target23]['passedATPercent'] == CODE_ACCEPTED,
                candidateGuides[target23]['passedTTTT'] == CODE_ACCEPTED,
                candidateGuides[target23]['passedSecondaryStructure'] == CODE_ACCEPTED,
                candidateGuides[target23]['passedAvoidLeadingT'] == CODE_ACCEPTED,
            ]):
                # mm10db rejected the guide
                candidateGuides[target23]['acceptedByMm10db'] = CODE_REJECTED
                failedCount += 1
            else:
                candidateGuides[target23]['acceptedByMm10db'] = CODE_ACCEPTED
                acceptedCount += 1
        printer(f'\t{acceptedCount} accepted.')
        printer(f'\t{failedCount} failed.')


def leadingT(candidateGuide: str) -> bool:
    return (candidateGuide[-2:] == 'GG' and candidateGuide[0] == 'T') or \
    (candidateGuide[:2] == 'CC' and candidateGuide[-1] == 'A')

# Function that calculates the AT% of a given sequence
def AT_percentage(candidateGuide: str) -> float:
    total = 0.0
    length = float(len(candidateGuide))
    for c in candidateGuide:
        if c in "AT":
            total += 1
    return 100.0*total/length

def polyT(candidateGuide: str) -> bool:
    return 'TTTT' in candidateGuide

switch_UT = str.maketrans('U', 'T')
# Function that replaces U with T in the sequence (to go back from RNA to DNA)
def transToDNA(rna: str) -> str:
    dna = rna.translate(switch_UT)
    return dna