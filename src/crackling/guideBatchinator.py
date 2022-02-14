import tempfile, csv
from crackling.Constants import *
from crackling.Helpers import *

class guideBatchinator():
    def __init__(self, batchSize:int):
        self.workingDir = tempfile.TemporaryDirectory()
        self.currentFile = tempfile.NamedTemporaryFile(mode='w',delete=False,dir=self.workingDir.name)
        self.csvWriter = csv.writer(self.currentFile, delimiter=',', quotechar='"', dialect='unix', quoting=csv.QUOTE_MINIMAL)
        self.batchFiles = []
        self.currentBatch = 0
        self.batchSize = batchSize
        self.entryCount = 0
        # Keep track of recorded Guides and Seqeunces
        self.candidateGuides = set()
        self.duplicateGuides = set()
        self.recordedSequences = set()
        self.numDuplicateGuides = 0
        self.numIdentifiedGuides = 0

    # Total number of batch files
    def __len__(self):
        return len(self.batchFiles)

    def __iter__(self):
        # yeild candidate guide dictionaries
        for file in self.batchFiles:
            self.currentBatch += 1
            # Create new candidate guide dictionary
            candidateGuides = {}
            # Load guides from temp file
            with open(file.name, 'r') as inputFp:
                # Create csv reader to parse temp file
                csvReader = csv.reader(inputFp, delimiter=',', quotechar='"', dialect='unix', quoting=csv.QUOTE_MINIMAL)
                # Rebuild dictonary from temp file
                for row in csvReader:
                    candidateGuides[row[0]] = DEFAULT_GUIDE_PROPERTIES.copy()
                    candidateGuides[row[0]]['seq'] = row[0]
                    if row[0] in self.duplicateGuides:
                        candidateGuides[row[0]]['header'] = CODE_AMBIGUOUS
                        candidateGuides[row[0]]['start'] = CODE_AMBIGUOUS
                        candidateGuides[row[0]]['end'] = CODE_AMBIGUOUS
                        candidateGuides[row[0]]['strand'] = CODE_AMBIGUOUS
                        candidateGuides[row[0]]['isUnique'] = CODE_REJECTED
                    else:
                        candidateGuides[row[0]]['header'] = row[1]
                        candidateGuides[row[0]]['start'] = row[2]
                        candidateGuides[row[0]]['end'] = row[3]
                        candidateGuides[row[0]]['strand'] = row[4]
            yield candidateGuides

    def recordGuide(self, guide:list):
        # Record the seqHeader
        self.recordedSequences.add(guide[1])
        # Increase guide count
        self.numIdentifiedGuides += 1
        # Check if guide has been seen before
        if guide[0] not in self.candidateGuides:
            # Record guide
            self.candidateGuides.add(guide[0])
            # Increase the entry count
            self.entryCount += 1
            # Check if a new file is needed
            if self.entryCount > self.batchSize:
                # Close current file
                self.currentFile.close()
                # Record file
                self.batchFiles.append(self.currentFile)
                # Create new file
                self.currentFile = tempfile.NamedTemporaryFile(mode='w',delete=False,dir=self.workingDir.name)
                # Update csv writer
                self.csvWriter = csv.writer(self.currentFile, delimiter=',', quotechar='"', dialect='unix', quoting=csv.QUOTE_MINIMAL)
                # Reset entry count
                self.entryCount = 1
            # Write entry
            self.csvWriter.writerow(guide)
        else:
            # Record duplicate guide
            if guide[0] not in self.duplicateGuides:
                # New duplicate guide add to list
                self.duplicateGuides.add(guide[0])
                # Increase duplicate guide count another time to include the original guide
                self.numDuplicateGuides += 1
            # Increase duplicate guide count
            self.numDuplicateGuides += 1

    def finaliseInput(self):
        # Ends the input processing. Dumps stats and removes redundant variables. Ready for iteration
        duplicatePercent = round(self.numDuplicateGuides / self.numIdentifiedGuides * 100.0, 3)
        printer(f'\tIdentified {self.numIdentifiedGuides:,} possible target sites in this file.')
        printer(f'\tOf these, {len(self.duplicateGuides):,} are not unique. These sites occur a total of {self.numDuplicateGuides} times.')
        printer(f'\tRemoving {self.numDuplicateGuides:,} of {self.numIdentifiedGuides:,} ({duplicatePercent}%) guides.')
        printer(f'\t{len(self.candidateGuides):,} distinct guides have been discovered so far.')
        # Close current file
        self.currentFile.close()
        # Record file
        self.batchFiles.append(self.currentFile)
        # Removes redundant variables
        del self.currentFile
        del self.csvWriter
        del self.batchSize
        del self.entryCount
        del self.candidateGuides
        del self.recordedSequences
        del self.numDuplicateGuides
        del self.numIdentifiedGuides
