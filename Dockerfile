# Use a Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run your application
CMD [ "python", "your_app.py" ]
