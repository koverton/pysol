#!/bin/bash -x
export SOLCLIENT_DIR=${SOLCLIENT_DIR:=.}

export PYTHONPATH=.:/usr/lib/python2.7:/usr/lib/python

export LD_LIBRARY_PATH=.:`pwd`/lib:$SOLCLIENT_DIR/lib 

export PATH=.:`pwd`/lib:$SOLCLIENT_DIR/lib:$PATH

