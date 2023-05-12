FROM python:3.10

# Set the working directory to /code
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Set the entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7865"]
