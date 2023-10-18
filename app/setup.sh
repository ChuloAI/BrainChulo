#!/bin/bash

# Install llama-cpp-python with CUBAS ON to allow gpu offloading in local
LLAMA_CUBLAS=1  pip install llama-cpp-python --force-reinstall --verbose

# Install experimental cpp guidance package
pip install git+https://github.com/Maximilian-Winter/guidance.git@313c726265c94523375b0dadd8954d19c01e709b

# Install andromeda-chain with no dependencies
pip install andromeda-chain==0.2.0 --no-deps

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing now..."
    
    # Installing poetry (this is the recommended way to install poetry)
    curl -sSL https://install.python-poetry.org | python3
else
    echo "Poetry is already installed."
fi

# Navigate to the directory containing pyproject.toml if not already there
# cd /path/to/directory/with/pyproject.toml  # Uncomment and replace with the correct path if needed

# Install dependencies from pyproject.toml using poetry
poetry install

echo "Installation completed!"
