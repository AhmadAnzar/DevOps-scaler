#!/bin/bash

mkdir -p test
cd test
echo "This is file1" > app.log
echo "This is file2" >> app.log
cat app.log