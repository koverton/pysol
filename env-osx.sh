#!/bin/bash -x
export SOLCLIENT_DIR=${SOLCLIENT_DIR:=.}

export PYTHONPATH=.:/usr/lib/python2.7:/usr/lib/python

export DYLIB_LIBRARY_PATH=$DYLIB_LIBRARY_PATH:$SOLCLIENT_DIR/lib.osx

export PATH=$SOLCLIENT_DIR/lib.osx:$PATH

