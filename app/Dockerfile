FROM python:3.10

# Set the working directory to /code
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Install PyTorch with GPU support
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Set the entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7865", "--reload"]
