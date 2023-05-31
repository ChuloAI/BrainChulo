FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Install Python
RUN apt update
RUN apt install -y python3 python3-pip && python3 --version

# Set the working directory to /code
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Install PyTorch with GPU support
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install git for bleeding-edge dependencies
RUN apt install -y git

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Expose library path to dynamic library linking
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/cuda-12/targets/x86_64-linux/lib

# Tell bitsandbytes to use CUDA 121
RUN ln -s /usr/local/cuda-12/targets/x86_64-linux/lib/libcudart.so.12 /usr/local/cuda-12/targets/x86_64-linux/lib/libcudart.so 

# Set the entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
