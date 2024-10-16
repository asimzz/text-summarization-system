FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app directory contents to the working directory
COPY ./backend/app /code/app
COPY ./backend/db /code/db
COPY ./backend/model /code/model
COPY ./backend/schemas /code/schemas
COPY ./backend/utils /code/utils

EXPOSE 8080

# Command to run the application
CMD ["fastapi", "run", "app/app.py", "--port", "8080"]
