#!/bin/bash

if [ $# -ne 1 ]; then
  echo "usage: ./upload.sh filename " 1>&2
  echo "loggedAt is yyyyMMddHHmmss" 1>&2
  exit 1
fi
JSON_NAME=$(basename $2).json

if [ ! ${PYMAVLINK:+foo} ]; then
  echo "please set PYMAVLINK env (ex PYMAVLINK=/home/bols/drone/dronekit-la/modules/mavlink/pymavlink/"
  echo "json name is ${JSON_NAME}"
  exit 1
fi


python ${PYMAVLINK}/tools/mavlogdump.py --format json2 --types RC*,ATT*,CTUN $2 > ${JSON_NAME}
#python ./to_json.py ${JSON_NAME}

rm ${JSON_NAME}
