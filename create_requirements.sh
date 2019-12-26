#!/bin/bash

pip install --user pipdeptree && \
    export PATH="/root/.local/bin:$PATH" && \
    echo $PATH && \
    pipdeptree --freeze  --warn silence | grep '==' | sed -e 's/ //g' > ./source/requirements.txt