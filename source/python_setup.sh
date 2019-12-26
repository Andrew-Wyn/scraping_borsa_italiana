#!/bin/bash

# eseguire in locale non tramite docker per incompatibilita con python alpine based

pip install --user pipdeptree && \
    export PATH="/root/.local/bin:$PATH" && \
    pipdeptree --freeze  --warn silence | grep '==' | sed -e 's/ //g' > requirements.txt && \
    pip install -r requirements.txt

rm requirements.txt