# use python 3.12 slim image as the base image
FROM python:3.12-slim

#set the working directory in the container
WORKDIR /app

# copy the requirements file to the working directory
COPY requirements.txt .

# install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application code to the working directory
COPY . .

# create a non-root user to run the application
RUN useradd -m appuser
# change ownership of the application files to the non-root user
RUN chown -R appuser:appuser /app

# switch to the non-root user
USER appuser

# expose the port that the application will run on
EXPOSE 9000

# set the command to run the application
CMD ["python", "flask-application.py"]