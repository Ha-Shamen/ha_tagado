FROM python:3.11
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
COPY . .
RUN poetry install 

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.web_service:app", "--bind", "0.0.0.0:7000"]