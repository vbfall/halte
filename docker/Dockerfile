# Parent image
FROM python:3.6

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U ./foundations/foundations-0.0.9-py3-none-any.whl
RUN pip install -U ./foundations/foundations_contrib-0.0.9-py3-none-any.whl
RUN pip install -U ./foundations/foundations_gcp-0.0.9-py3-none-any.whl
RUN pip install -U ./foundations/foundations_internal-0.0.9-py3-none-any.whl
RUN pip install -U ./foundations/foundations_rest_api-0.0.9-py3-none-any.whl
RUN pip install -U ./foundations/foundations_ssh-0.0.9-py3-none-any.whl

# How do you map a port out of the container to host?
# So this container can have access to Redis on another one.

# Run <app.py> when the container launches or run container interactively
CMD ["python", "./driver.py"]
