#!/bin/sh  

pip install pytest
pip install pandas

echo "Execute the pipeline ..."
python project/data/datapipline_script.py

echo "Test if pipeline works correctly ..."
pytest project/data/testpipline.py