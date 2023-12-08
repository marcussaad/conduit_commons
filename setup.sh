#!/bin/sh

if [ `uname` = "Linux" ] ;
then
	sudo apt-get install librdkafka-dev
fi
if [ `uname` = "Darwin" ] ;
then
    brew install librdkafka
	export C_INCLUDE_PATH=/opt/homebrew/Cellar/librdkafka/2.2.0/include
   	export LIBRARY_PATH=/opt/homebrew/Cellar/librdkafka/2.2.0/lib
fi

python3.10 -m venv  ~/.venvs/conduit-commons
. ~/.venvs/conduit-commons/bin/activate
pip install -r conduit_commons/requirements.txt
pre-commit install
