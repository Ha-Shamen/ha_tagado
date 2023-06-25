FROM python:3.11
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
COPY . .
RUN poetry install 

CMD [ "python", "./app/data_service.py"]