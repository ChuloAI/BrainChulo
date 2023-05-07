FROM python:3.10

# Set the working directory to /app
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./app /code/app

# Set the entrypoint
CMD ["gradio", "app/main.py"]
