#!/bin/bash

if [ "${1}" != "" ]; then
  FILENAME="${1%%.*}.ged"
  python CSV2GEDCOM.py "${1}" > "${FILENAME}"
  echo "Created ${FILENAME}"
fi
