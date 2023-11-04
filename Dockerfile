# Use Python 3.10.9 as the parent image
FROM python:3.10.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable (if needed)
# ENV MY_VAR=my_value

# Copy start.sh and give it the required permissions
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Run start.sh when the container starts
CMD ["/app/start.sh"]