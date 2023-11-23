FROM python:3.8.10-slim
ENV PYTHONUNBUFFERED=1
# Relevant folder
ARG FOLDER=/api

# Create a folder
RUN mkdir -p $FOLDER

# Install packages
COPY . $FOLDER/
WORKDIR $FOLDER
RUN pip install -r requirements.txt


CMD uvicorn chat:app --port=8000 --host=0.0.0.0