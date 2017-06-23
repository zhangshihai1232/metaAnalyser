#!/bin/bash
FILE_PATH=$1

while read line || [[ -n ${line} ]]; do
    echo "$line"
done < $FILE_PATH