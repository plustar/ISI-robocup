#!/bin/bash
cd /home/isi/2017_ws/src/imgpcl/
enscript -p sed_test.ps result.txt 
ps2pdf sed_test.ps sed_test.pdf 
convert operator_gender_detect.jpg gender_detect.jpg sed_test.pdf  Kamerider-Try-Timestamp.pdf

exit 0
