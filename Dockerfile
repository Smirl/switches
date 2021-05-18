FROM python:3.9.5-alpine
WORKDIR /src
RUN apk --no-cache add build-base postgresql-dev gcc musl-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "switches.py"]
