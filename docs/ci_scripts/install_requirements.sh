#!/bin/bash

while getopts d:r:p: option
do
  case "${option}"
  in
    d) DIRECTORY=${OPTARG};;
    r) REQ_FILE=${OPTARG};;
    p) INSTALL_PATH=${OPTARG};;
    *) echo "usage: $0 [-d] [-r]" >&2
           exit 1 ;;
  esac
done

if [ "${INSTALL_PATH}" != "" ]
then
  FLAG_INSTALL_PATH=" --target ${INSTALL_PATH}"
  for ver in $(ls -d ../../${DIRECTORY}/*/ | awk -F'/' '{print $4}' | grep '^v[1-9]\+')
  do
    LAYER_PATH="../../${DIRECTORY}/${ver}/${INSTALL_PATH}"
    pip3 install -r "../../${DIRECTORY}/${ver}/requirements/${REQ_FILE}" --target "./${LAYER_PATH}/"
  done
else
  for ver in $(ls -d ../../${DIRECTORY}/*/ | awk -F'/' '{print $4}' | grep '^v[1-9]\+')
  do
    pip3 install -r "../../${DIRECTORY}/${ver}/requirements/${REQ_FILE}"
  done
fi

