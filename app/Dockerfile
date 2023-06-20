FROM python:3.10

# Set the working directory to /code
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Set your environment variables
ENV BASE_URL="import.meta.env.VITE_BACKEND_BASE_URL"
ENV DOCKER_ENV=true

COPY ./requirements.txt /code/requirements.txt
RUN LLAMA_CUBLAS=1 CMAKE_ARGS=-DLLAMA_CUBLAS=on FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall --verbose
RUN pip3 install git+https://github.com/Maximilian-Winter/guidance.git@313c726265c94523375b0dadd8954d19c01e709b
RUN pip3 install -r requirements.txt

COPY . .

# Set the entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7865", "--reload"]
