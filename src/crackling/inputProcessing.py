from crackling import ConfigManager
from crackling.Helpers import *
from crackling.Constants import *
from crackling.guideBatchinator import guideBatchinator

import os, re, csv

# Define patterns for guide matching
pattern_forward = re.compile(r'(?=([ATCG]{21}GG))')
pattern_reverse = re.compile(r'(?=(CC[ACGT]{21}))')

# Helper function
def processSequence(seqHeader, seq):
    # New sequence deteced, process sequence
    # once for forward, once for reverse
    for pattern, strand, seqModifier in [
        [pattern_forward, '+', lambda x : x],
        [pattern_reverse, '-', lambda x : rc(x)]
    ]:
        for m in pattern.finditer(seq):
            target23 = seqModifier(seq[m.start() : m.start() + 23])
            yield [target23, seqHeader,  m.start(),  m.start() + 23, strand]

def processInput(configMngr: ConfigManager):
    ###################################
    ##   Processing the input file   ##
    ###################################
    printer('Analysing files...')

    # Keep track of overall progress
    totalSizeBytes = configMngr.getDatasetSizeBytes()
    completedSizeBytes = 0

    # Create Batchinator to process the input file into batches
    inputBatchinator = guideBatchinator(int(configMngr['input']['batch-size']))
    printer(f'Batchinator is writing to: {inputBatchinator.workingDir.name}')

    # Iterate through input files
    for seqFilePath in configMngr.getIterFilesToProcess():
        printer(f'Identifying possible target sites in: {seqFilePath}')
        # Detect file type, Fasta or plain text
        with open(seqFilePath, 'r') as inFile:
            # Read first line to detect header line
            firstLine = inFile.readline().strip()
            # Sequence header detected, file is Fasta format
            if firstLine[0] == '>':
                # Initialize seqHeader and iterate through file
                seqHeader = firstLine[1:]
                seq = []
                # Process fasta, Iterate through file ONCE by continuosly seeking for seqeunces and process on detection of new
                for line in inFile:
                    line = line.strip()
                    # Header line detected, process current seq
                    if line[0] == '>':
                        # A new header line detected, process previous sequence
                        if seqHeader not in inputBatchinator.recordedSequences:
                            # Concat string once using join for best performance
                            seq = ''.join(seq)
                            # Process new seq
                            for guide in processSequence(seqHeader, seq):
                                inputBatchinator.recordGuide(guide)
                        # Update sequence and sequence header and continue until a new header is detected
                        seqHeader = line[1:]
                        seq = []
                    else:
                        # Concatinating once, append to list should improve speed
                        seq.append(line)
                # EOF reached, process the last seq
                # Concat string once using join for best performance
                seq = ''.join(seq)
                # Process new seq
                for guide in processSequence(seqHeader, seq):
                    inputBatchinator.recordGuide(guide)
            # File is plain text (Assuming 1 seqeunce per line)
            else:
                for line in inFile:
                    line = line.strip()
                    # Process new seq
                    for guide in processSequence('', seq):
                        inputBatchinator.recordGuide(guide)

        # Update overall process
        completedSizeBytes += os.path.getsize(seqFilePath)
        completedPercent = round(completedSizeBytes / totalSizeBytes * 100.0, 3)
        printer(f'\tExtracted from {completedPercent}% of input')

    # Finalise the batchinator, prints report, deletes redundant variables, closes current file etc.
    inputBatchinator.finaliseInput()

    # Write header line for output file
    with open(configMngr['output']['file'], 'a+') as fOpen:
        csvWriter = csv.writer(fOpen, delimiter=configMngr['output']['delimiter'],
                        quotechar='"',dialect='unix', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(DEFAULT_GUIDE_PROPERTIES_ORDER)

    # Return batchinator 
    return inputBatchinator