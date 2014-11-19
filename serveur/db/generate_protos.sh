#!/bin/bash
# Generates the python files from the *.proto description files.
# WARNING: don't modify the generated *_pb2.py files.
protoc -I=. --python_out=. *.proto
