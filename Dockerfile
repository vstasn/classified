FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /classified
WORKDIR /classified
COPY requirements.txt /classified/
RUN pip install -r requirements.txt
COPY . /classified/
