FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Expose the port that the app will run on
EXPOSE 7860

# Set the entrypoint to the main Python file
CMD ["gradio", "main.py"]
