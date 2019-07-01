#!/usr/bin/env bash
python_path=/opt/Python-3.6.0/bin/python3
while :
do
    content=`ps -aux|grep baidu_ocr.py|grep -v grep| awk '{print $2}'`
    if [[ -z $content ]]
    then
        $python_path baidu_ocr.py
    else
        continue
    fi
done      

