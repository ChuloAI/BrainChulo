# Use an official node runtime as a parent image
FROM node:18.16.0

# Set the working directory
WORKDIR /code

# Copy package.json and package-lock.json to the container's /code directory
COPY package*.json /code

# Install any needed packages specified in package.json
RUN npm install

# Copy the rest of the code to the container's /code directory
COPY . .

EXPOSE 5173

# Specify the command to run when the container starts
ENTRYPOINT ["/entrypoint.sh"]

