#!/bin/bash

# Install llama-cpp-python with CUBAS ON to allow gpu offloading in local
LLAMA_CUBLAS=1  pip install llama-cpp-python  --force-reinstall --verbose

# Install experimental cpp guidance package
pip install git+https://github.com/Maximilian-Winter/guidance.git@313c726265c94523375b0dadd8954d19c01e709b

# Install andromeda-chain with no dependencies
pip install andromeda-chain==0.2.0 --no-deps

# Install packages from requirements_local.txt
pip install -r requirements_local.txt
