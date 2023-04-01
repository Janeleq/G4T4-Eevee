FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./Backend/make_transaction.py .
CMD [ "python", "./Backend/make_transaction.py" ]
