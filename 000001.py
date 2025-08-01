#!/bin/bash

# Set up conda
source /apps/mvp/conda/mini-conda-base/etc/profile.d/conda.sh

# Clone the environment
conda create --name llm-pipeline-server --clone vnlp-torch-transformer-cuda-test13 -y

# Activate the cloned environment and verify
conda activate llm-pipeline-server
echo "✅ Environment cloned successfully. Packages in llm-pipeline-server:"
conda list