#!/bin/bash

# Update version numbers in executables and build scripts
# Do not put a "v" in front of the version number
# Example Usage:
# ./ver_update.sh 0.6.2 0.6.3

OLDVER=$1
NEWVER=$2

FILELIST="setup.py
	  ncbimeta/NCBImeta.py
	  ncbimeta/NCBImetaAnnotateConcatenate.py
	  ncbimeta/NCBImetaAnnotateReplace.py
	  ncbimeta/NCBImetaExport.py
	  ncbimeta/NCBImetaJoin.py"

for file in `ls $FILELIST`;
do
    echo "Updating $file from v$OLDVER to v$NEWVER";
    sed -i "s/$OLDVER/$NEWVER/g" $file;
done
