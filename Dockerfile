FROM python:2.7-alpine
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt
CMD ["python", "src/setup.py", "py2exe"]
