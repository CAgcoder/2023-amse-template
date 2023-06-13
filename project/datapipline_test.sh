#!/bin/sh  

pip install pytest

echo "Execute the pipeline ..."
python ./data/datapipline_script.py

echo "Test if pipeline works correctly ..."
pytest ./data/testpipline.py