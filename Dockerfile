# Parent image
FROM python:2.7-slim

# Set the working directory
WORKDIR /

# Copy the current directory contents into the container WORKDIR
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variables
# ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]