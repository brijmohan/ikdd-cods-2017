#!/bin/bash

virtualenv venv
. venv/bin/activate

pip install https://github.com/kpu/kenlm/archive/master.zip
git clone https://github.com/irshadbhat/litcm.git

pip install -r bin/requirements.txt
