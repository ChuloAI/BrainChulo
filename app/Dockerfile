FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Install Python
RUN apt update
RUN apt install -y python3 python3-pip && python3 --version

# Set the working directory to /code
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Install PyTorch with GPU support
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


# Set the entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7865", "--reload"]
