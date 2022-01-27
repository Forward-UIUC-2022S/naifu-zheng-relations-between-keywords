#!/bin/bash
WD=$1
KEYWORD=$2
QUERY_KEYWORD=$3

cd $WD/henrik-tseng-meaningful-relations-between-keywords

source env/bin/activate
python3 main.py "$KEYWORD" "$QUERY_KEYWORD" 