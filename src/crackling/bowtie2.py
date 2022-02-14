from crackling.ConfigManager import ConfigManager
from crackling.Constants import *
from crackling.Helpers import *
from crackling.Paginator import Paginator
import ast

def bowtie2(candidateGuides: dict, configMngr: ConfigManager):
    if (configMngr['offtargetscore'].getboolean('enabled')):
            ###############################################
            ##         Using Bowtie for positioning      ##
            ###############################################
            printer('Bowtie analysis.')
            testedCount = 0
            failedCount = 0
            pgLength = configMngr['bowtie2'].getint('page-length')
            for pgIdx, pageCandidateGuides in Paginator(
                filterCandidateGuides(configMngr, candidateGuides, MODULE_SPECIFICITY),
                pgLength
            ):
                if pgLength > 0:
                    printer(f'\tProcessing page {(pgIdx+1)} ({pgLength:,} per page).')

                printer('\tConstructing the Bowtie input file.')
                tempTargetDict_offset = {}
                guidesInPage = 0
                with open(configMngr['bowtie2']['input'], 'w') as fWriteBowtie:
                    for target23 in pageCandidateGuides:
                        similarTargets = [
                            target23[0:20] + 'AGG',
                            target23[0:20] + 'CGG',
                            target23[0:20] + 'GGG',
                            target23[0:20] + 'TGG',
                            target23[0:20] + 'AAG',
                            target23[0:20] + 'CAG',
                            target23[0:20] + 'GAG',
                            target23[0:20] + 'TAG'
                        ]
                        for seq in similarTargets:
                            fWriteBowtie.write(seq + '\n')
                            tempTargetDict_offset[seq] = target23
                        guidesInPage += 1
                printer(f'\t\t{guidesInPage:,} guides in this page.')

                runner('{} -x {} -p {} --reorder --no-hd -t -r -U {} -S {}'.format(
                        configMngr['bowtie2']['binary'],
                        configMngr['input']['bowtie2-index'],
                        configMngr['bowtie2']['threads'],
                        configMngr['bowtie2']['input'],
                        configMngr['bowtie2']['output']
                    ),
                    shell=True,
                    check=True
                )

                printer('\tStarting to process the Bowtie results.')
                inFile = open(configMngr['bowtie2']['output'], 'r')
                bowtieLines = inFile.readlines()
                inFile.close()
                i=0
                while i<len(bowtieLines):
                    nb_occurences = 0
                    # we extract the read and use the dictionary to find the corresponding target
                    line = bowtieLines[i].rstrip().split('\t')
                    chr = line[2]
                    pos = ast.literal_eval(line[3])
                    read = line[9]
                    seq = ''
                    if read in tempTargetDict_offset:
                        seq = tempTargetDict_offset[read]
                    elif rc(read) in tempTargetDict_offset:
                        seq = tempTargetDict_offset[rc(read)]
                    else:
                        print('Problem? '+read)
                    if seq[:-2] == 'GG':
                        candidateGuides[seq]['bowtieChr'] = chr
                        candidateGuides[seq]['bowtieStart'] = pos
                        candidateGuides[seq]['bowtieEnd'] = pos + 22
                    elif rc(seq)[:2] == 'CC':
                        candidateGuides[seq]['bowtieChr'] = chr
                        candidateGuides[seq]['bowtieStart'] = pos
                        candidateGuides[seq]['bowtieEnd'] = pos + 22
                    else:
                        print('Error? '+seq)
                        quit()
                    # we count how many of the eight reads for this target have a perfect alignment
                    for j in range(i,i+8):
                        # http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#sam-output
                        # XM:i:<N>    The number of mismatches in the alignment. Only present if SAM record is for an aligned read.
                        # XS:i:<N>    Alignment score for the best-scoring alignment found other than the alignment reported.
                        if 'XM:i:0' in bowtieLines[j]:
                            nb_occurences += 1
                            # we also check whether this perfect alignment also happens elsewhere
                            if 'XS:i:0'  in bowtieLines[j]:
                                nb_occurences += 1
                    # if that number is at least two, the target is removed
                    if nb_occurences > 1:
                        # increment the counter if this guide has not already been rejected by bowtie
                        if candidateGuides[seq]['passedBowtie'] != CODE_REJECTED:
                            failedCount += 1
                        candidateGuides[seq]['passedBowtie'] = CODE_REJECTED
                    else:
                        candidateGuides[seq]['passedBowtie'] = CODE_ACCEPTED
                    # we continue with the next target
                    i+=8
                    testedCount += 1
                # we can remove the dictionary
                del tempTargetDict_offset
            printer(f'\t{failedCount:,} of {testedCount:,} failed here.')