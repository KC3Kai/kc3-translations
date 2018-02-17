#!/usr/bin/env python3

import sys
import json
from collections import OrderedDict

# TODO & NOTE: don't apply it on English version, for now.

indent = "\t"

descToId = {
    "Intro" : 1,
    "Library" : 25,
    "Poke(1)" : 2,
    "Poke(2)" : 3,
    "Poke(3)" : 4,
    "Married" : 28,
    "Wedding" : 24,
    "Ranking" : 8,
    "Join" : 13,
    "Equip(1)" : 9,
    "Equip(2)" : 10,
    "Equip(3)" : 26,
    "Supply" : 27,
    "Docking(1)" : 11,
    "Docking(2)" : 12,
    "Construction" : 5,
    "Return" : 7,
    "Sortie" : 14,
    "Battle" : 15,
    "Attack" : 16,
    "Yasen(1)" : 18,
    "Yasen(2)" : 17,
    "MVP" : 23,
    "Damaged(1)" : 19,
    "Damaged(2)" : 20,
    "Damaged(3)" : 21,
    "Sunk" : 22,
    "Idle" : 29,
    "Repair" : 6,
    "H0000":30, "H0100":31, "H0200":32, "H0300":33,
    "H0400":34, "H0500":35, "H0600":36, "H0700":37,
    "H0800":38, "H0900":39, "H1000":40, "H1100":41,
    "H1200":42, "H1300":43, "H1400":44, "H1500":45,
    "H1600":46, "H1700":47, "H1800":48, "H1900":49,
    "H2000":50, "H2100":51, "H2200":52, "H2300":53
}

# convert values to strings
keys = descToId.keys()
for k in keys:
    descToId[k] = str(descToId[k])

idToDesc = {}
for k,v in descToId.items():
    idToDesc[v] = k

def helpAndQuit():
    print( "Usage:" )
    print( "  {} desc <quote-file-A> <quote-file-B>".format(sys.argv[0]))
    print( "or" )
    print( "  {} id <quote-file-A> <quote-file-B>".format(sys.argv[0]))
    sys.exit(1)

if __name__ == '__main__':
    if len( sys.argv ) == 4:
        mode, fileA, fileB = sys.argv[1:]
        convertTable = {}
        if mode == "desc":
            convertTable = idToDesc
        elif mode == "id":
            convertTable = descToId
        else:
            helpAndQuit()

        quoteData = None
        with open(fileA,encoding='utf_8_sig') as f:
            quoteData = json.load(f, object_pairs_hook=OrderedDict)

        assert quoteData is not None, "something went wrong when loading / reading file."
        for k,v in quoteData.items():
            masterKey = None
            try:
                masterKey = int(k)
            except ValueError:
                continue
            newQuoteEntry = OrderedDict()
            for qKey, qVal in v.items():
                qKey = str(qKey)
                qKey = convertTable.get(qKey, qKey)
                newQuoteEntry[qKey] = qVal

            quoteData[k] = newQuoteEntry

        with open(fileB,"w",encoding='utf_8_sig') as f:
            json.dump(quoteData, f, indent=indent, ensure_ascii=False)

    else:
        helpAndQuit()
