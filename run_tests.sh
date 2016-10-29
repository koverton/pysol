#!/bin/bash -x

# Executes test code against external addresses of demo-tr server

. ./env.sh

python tests/data_test.py

python tests/direct_test.py properties/demotr-ext.properties

python tests/string_payload_test.py properties/demotr-ext.properties

python tests/object_payload_test.py properties/demotr-ext.properties

python tests/blocking_receiver_test.py properties/demotr-ext.properties

python tests/persistent_test.py properties/demotr-ext.properties

python tests/persistent_ack_test.py properties/demotr-ext.properties

python tests/persistent_streaming_test.py properties/demotr-ext.properties

# python tests/cache_test.py properties/demotr-ext.properties
