#!/bin/sh

TOOL_PATH=../../tools

TMP1=`tempfile`
wget http://api.kcwiki.moe/subtitles -O $TMP1

TMP2=`tempfile`

${TOOL_PATH}/kcwikizh-subtitle-merge.py $TMP1 quotes.json $TMP2

${TOOL_PATH}/quotes-minify.py ${TOOL_PATH}/remodelGroups.json $TMP2 quotes.json

rm $TMP1
rm $TMP2
