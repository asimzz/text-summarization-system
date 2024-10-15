FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app directory contents to the working directory
COPY ./app_ui.py /code/app_ui.py

EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app_ui.py"]