#!/usr/bin/env python3

import sys
import glob
import os
import json

def onDiffFromList(a,b):
    return "No difference" if a == b else "Missing {} items".format(a-b)

def onExtractFromObj(d):
    return set(d.keys())

def onDiffFromObj(a,b):
    diff = a-b
    return "No difference" if len(diff) == 0 else "Missing items: {}".format(diff)

handlers = \
    { dict: [onExtractFromObj, onDiffFromObj  ],
      list: [len, onDiffFromList ]
    }

if __name__ == '__main__':
    if len( sys.argv ) == 3:
        dirA, dirB = sys.argv[1:]
        filesA = set(glob.glob(dirA + "/*.json"))
        for fileA in filesA:
            fileName = os.path.basename(fileA)
            fileB = os.path.join(dirB,fileName)
            if os.path.isfile( fileB ):
                def loadFile(fn):
                    with open(fn,"r") as f:
                        return json.load(f)
                print("Comparing {} and {}".format(fileA,fileB))
                jsonA, jsonB = loadFile(fileA), loadFile(fileB)
                extract, diff = handlers[jsonA.__class__]
                resultA, resultB = extract(jsonA), extract(jsonB)
                print("  Difference: {}".format( diff(resultA,resultB) ) )
            else:
                print("Missing file: {}".format(fileName))
    else:
        print( "{} <dirA> <dirB>".format(sys.argv[0]))
