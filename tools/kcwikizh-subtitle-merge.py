#!/usr/bin/env python3

import sys
import json
from collections import OrderedDict

# merge subtitles from kcwiki format into quotes.json
# * quotes.json must be using descriptive keys

# the latest subtitles.json can be downloaded from:
# http://api.kcwiki.moe/subtitles
# See: https://github.com/kcwikizh/poi-plugin-subtitle/issues/3#issuecomment-207950136

# options
indent = "\t"
allowOverwrite = True

descToId = OrderedDict( [
    ("Intro", 1),
    ("Library", 25),
    ("Poke(1)", 2),
    ("Poke(2)", 3),
    ("Poke(3)", 4),
    ("Married", 28),
    ("Wedding", 24),
    ("Ranking", 8),
    ("Join", 13),
    ("Equip(1)", 9),
    ("Equip(2)", 10),
    ("Equip(3)", 26),
    ("Supply", 27),
    ("Docking(1)", 11),
    ("Docking(2)", 12),
    ("Construction", 5),
    ("Return", 7),
    ("Sortie", 14),
    ("Battle", 15),
    ("Attack", 16),
    ("Yasen(1)", 18),
    ("Yasen(2)", 17),
    ("MVP", 23),
    ("Damaged(1)", 19),
    ("Damaged(2)", 20),
    ("Damaged(3)", 21),
    ("Sunk", 22),
    ("Idle", 29),
    ("Repair", 6),
    ("H0000",30), ("H0100",31), ("H0200",32), ("H0300",33),
    ("H0400",34), ("H0500",35), ("H0600",36), ("H0700",37),
    ("H0800",38), ("H0900",39), ("H1000",40), ("H1100",41),
    ("H1200",42), ("H1300",43), ("H1400",44), ("H1500",45),
    ("H1600",46), ("H1700",47), ("H1800",48), ("H1900",49),
    ("H2000",50), ("H2100",51), ("H2200",52), ("H2300",53)
])

# convert values to strings
keys = descToId.keys()
for k in keys:
    descToId[k] = str(descToId[k])

idToDesc = {}
for k,v in descToId.items():
    idToDesc[v] = k

def helpAndQuit():
    print( "Usage:" )
    print( "  {} <kcwiki-subtitles.json> <quote-file-A> <quote-file-B>".format(sys.argv[0]))
    sys.exit(1)

def loadFileToOrderedList(fn):
    content = None
    with open(fn,encoding='utf_8_sig') as f:
        content = json.load(f, object_pairs_hook=OrderedDict)
    assert content is not None, "something went wrong when loading / reading file."
    return content

if __name__ == '__main__':
    if len( sys.argv ) == 4:
        kcSubtitlesF, fileA, fileB = sys.argv[1:]

        kcSubs = loadFileToOrderedList(kcSubtitlesF)
        quoteData = loadFileToOrderedList(fileA)

        emptyCnt = 0
        identicalCnt = 0
        differentCnt = 0
        missingCnt = 0

        if allowOverwrite:
            mode = "Overwritten"
        else:
            mode = "Skipped"

        for k,v in kcSubs.items():
            masterKey = None
            try:
                masterKey = int(k)
            except ValueError:
                continue

            # "k" is a string
            lines = quoteData.get(k,OrderedDict())
            # use values in "v" to update lines
            for qNumKey,qLine in v.items():
                qLine = qLine.strip()
                if qLine == "":
                    emptyCnt = emptyCnt + 1
                    continue

                qDescKey = idToDesc[ qNumKey ]
                if qDescKey in lines:
                    if lines[qDescKey] == qLine:
                        identicalCnt = identicalCnt + 1
                    else:
                        differentCnt = differentCnt + 1
                        print("Detecting Differernce:")
                        print("  location: masterId={0}, quote={1}".format(masterKey, qDescKey))
                        print("  quotes: {0}".format(lines[qDescKey]))
                        print("  kcwiki: {0}".format(qLine))
                        if allowOverwrite:
                            print("Overwriting original content.")
                            lines[qDescKey] = qLine
                        else:
                            print("Skipping different content.")
                else:
                    missingCnt = missingCnt + 1
                    lines[qDescKey] = qLine
            quoteData[k] = lines

        print("Update summary:")
        print("  Empty Items: {0}".format(emptyCnt))
        print("  Identical Items: {0}".format(identicalCnt))
        print("  Different Items: {0} ({1})".format(differentCnt,mode))
        print("  Missing Items: {0}".format(missingCnt))
        with open(fileB,"w",encoding='utf_8_sig') as f:
            json.dump(quoteData, f, indent=indent, ensure_ascii=False)
    else:
        helpAndQuit()
