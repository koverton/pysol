#!/bin/bash

# Executes test code against internal addresses of vmr server

. ./env.sh

echo "==================================================="
echo "===================DATA   TEST====================="
echo "==================================================="
python tests/data_test.py

echo "==================================================="
echo "===================DIRECT TEST====================="
echo "==================================================="
python tests/direct_test.py properties/vmr.properties

echo "==================================================="
echo "===================STRING PAYLOAD TEST============="
echo "==================================================="
python tests/string_payload_test.py properties/vmr.properties

echo "==================================================="
echo "===================OBJECT PAYLOAD TEST============="
echo "==================================================="
python tests/object_payload_test.py properties/vmr.properties

echo "==================================================="
echo "===================BLOCKING RECV TEST=============="
echo "==================================================="
python tests/blocking_receiver_test.py properties/vmr.properties

echo "==================================================="
echo "===================PERSISTENT TEST================="
echo "==================================================="
python tests/persistent_test.py properties/vmr.properties

echo "==================================================="
echo "===================PERSISTENT ACK TEST============="
echo "==================================================="
python tests/persistent_ack_test.py properties/vmr.properties

echo "==================================================="
echo "===================PERSISTENT STREAMING TEST======="
echo "==================================================="
python tests/persistent_streaming_test.py properties/vmr.properties

# python tests/cache_test.py properties/vmr.properties
