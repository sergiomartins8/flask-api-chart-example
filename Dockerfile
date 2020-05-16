FROM python:3.7-slim
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN chmod 644 api.py
EXPOSE 8080
CMD ["python", "api.py"]