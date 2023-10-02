#!/bin/bash

#
# Assume you have conda installed
#
# Usage:
#   
#     sbatch --ntasks-per-node=1 --mem=32G inference_server_SHARED.sh meta/Llama-2-7b-chat-hf
#     sbatch --ntasks-per-node=2 --mem=64G inference_server_SHARED.sh meta/Llama-2-13b-chat-hf
#     sbatch --ntasks-per-node=8 --mem=192G inference_server_SHARED.sh meta/Llama-2-70b-chat-hf
#

#SBATCH --gpus-per-task=rtx8000:1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:15:00
#SBATCH --ntasks-per-node=1
#SBATCH --mem=32G

MODEL="$1"

export MILA_WEIGHTS="/network/weights/"

cd $SLURM_TMPDIR

#
#   Fix problem with conda saying it is not "init properly"
#
CONDA_EXEC="$(which conda)"
CONDA_BASE=$(dirname $CONDA_EXEC)
source $CONDA_BASE/../etc/profile.d/conda.sh

#
#   Create a new environment
#
conda create --prefix ./env python=3.9 -y 
conda activate ./env
pip install vllm


#
#    Setup shared cache to avoid redownloading weights
#
python /network/weights/shared_cache/setup.py 

export HF_HOME=$HOME/scratch/cache/huggingface
export HF_DATASETS_CACHE=$HOME/scratch/cache/huggingface/datasets
export TORCH_HOME=$HOME/scratch/cache/torch

#
#   Save metadata for retrival
#
PORT=9123
HOST="$(hostname)"
NAME="$WEIGHTS/$MODEL"

scontrol update job $SLURM_JOB_ID comment="model=$MODEL|host=$HOST|port=$PORT|shared=y"


# 
#   Launch Server
#
python -m vllm.entrypoints.openai.api_server     \
     --host $HOST                                \
     --port $PORT                                \
     --model "$MODEL"                            \
     --tensor-parallel-size $SLURM_NTASKS_PER_NODE

