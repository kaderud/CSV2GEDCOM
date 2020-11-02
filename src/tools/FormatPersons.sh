#!/bin/bash

INPUTFILE="PRINTPER.csv"
OUTPUTFILE="persons.csv"
TEMPFILE=".${INPUTFILE%%.*}"

if [[ -f "${INPUTFILE}" ]]; then
    python FormatCSV.py ${INPUTFILE} > ${TEMPFILE}
    tr -d '\032' < ${TEMPFILE} > ${OUTPUTFILE}
    sed -i '/^$/d' ${OUTPUTFILE}
    rm ${TEMPFILE}
    echo Created [${OUTPUTFILE}]
else
    echo [${INPUTFILE}] does not exist!
fi
