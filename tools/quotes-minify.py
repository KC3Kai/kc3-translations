#!/usr/bin/env python3

import sys
import json
from collections import OrderedDict

# minify quotes by:
# * removing empty lines
# * removing duplicated lines (if one's previous model has the same line)

# requires "remodelGroups.json" file to work.
# you can generate one from saving result content of "RemodelDb.dumpRemodelGroups()" to a file

# options
indent = "\t"

def helpAndQuit():
    print( "Usage:" )
    print( "  {} <remodelGroups.json> <quote-file-A> <quote-file-B>".format(sys.argv[0]))
    sys.exit(1)

def loadFileToOrderedList(fn):
    content = None
    with open(fn,encoding='utf_8_sig') as f:
        content = json.load(f, object_pairs_hook=OrderedDict)
    assert content is not None, "something went wrong when loading / reading file."
    return content

if __name__ == '__main__':
    if len( sys.argv ) == 4:
        remodelGroupsF, fileA, fileB = sys.argv[1:]

        remodelGroups = loadFileToOrderedList(remodelGroupsF)
        quoteData = loadFileToOrderedList(fileA)

        removeCnt = 0
        emptyCnt = 0

        # first scan: just removing empty lines
        for k,lines in quoteData.items():
            masterKey = None
            try:
                masterKey = int(k)
            except ValueError:
                continue
            keysToDel = []
            for qKey,qLine in lines.items():
                qLine = qLine.strip()
                if qLine == "":
                    emptyCnt = emptyCnt + 1
                    keysToDel.append(qKey)
            for key in keysToDel:
                del lines[key]

        # considering remodel groups backwards
        for groupInfo in remodelGroups.values():
            group = groupInfo["group"]
            # pairs of current ship master id and its previous remodel's
            for curShipId, preShipId in reversed(list(zip(group[1:],group))):
                curShipIdS, preShipIdS = str(curShipId), str(preShipId)
                if curShipIdS in quoteData and preShipIdS in quoteData:
                    curShipLines = quoteData[ curShipIdS ]
                    preShipLines = quoteData[ preShipIdS ]
                    keysToDel = []
                    for qKey, qLine in curShipLines.items():
                        if qKey in preShipLines:
                            if preShipLines[qKey] == qLine:
                                removeCnt = removeCnt + 1
                                keysToDel.append(qKey)
                    for key in keysToDel:
                        del curShipLines[key]

        print("Safely Removed Non-empty Lines: {0}".format(removeCnt));
        print("Safely Removed Empty Lines: {0}".format(emptyCnt));
        with open(fileB,"w",encoding='utf_8_sig') as f:
            json.dump(quoteData, f, indent=indent, ensure_ascii=False)
    else:
        helpAndQuit()
