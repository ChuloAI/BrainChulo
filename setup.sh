#!/bin/bash
sudo app/setup.sh

# Clone the text-generation-webui repository
if [ ! -d "text-generation-webui" ]; then
    git clone https://github.com/oobabooga/text-generation-webui
    if [ $? -ne 0 ]; then
        echo "Failed to clone text-generation-webui repository"
        exit 1
    fi
else
    echo "text-generation-webui directory already exists"
fi

# Check if bctxtgen environment already exists
conda info --envs | grep bctxtgen
if [ $? -eq 0 ]; then
    echo "Conda environment bctxtgen already exists"
else
    # Create a new Conda environment
    conda create -y -n bctxtgen python=3.10.9
    if [ $? -ne 0 ]; then
        echo "Failed to create Conda environment"
        exit 1
    fi
fi

# Activate the Conda environment
source activate bctxtgen

# Navigate to the cloned repository and install the requirements
cd text-generation-webui

# Check if model directory already exists
if [ -d "models" ]; then
    echo "Model directory already exists"
else
    pip install -r requirements.txt
    python download-model.py TheBloke/orca_mini_v2_7B-GPTQ
fi

# Check if repositories directory already exists
if [ -d "repositories" ]; then
    echo "Repositories directory already exists"
else
    # Create a new directory and clone the exllama repository into it
    mkdir -p ../repositories
    cd ../repositories
    git clone https://github.com/turboderp/exllama
fi

python server.py --listen --model ./models/TheBloke_orca_mini_v2_7B-GPTQ --model_type llama  --api  --verbose --loader exllama 
