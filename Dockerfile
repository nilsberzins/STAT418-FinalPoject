#lightweight version of python
FROM python:3.12-slim 

#EXPOSE 5001
EXPOSE 5001

WORKDIR /server

# Copy requirements.txt in so that pip can access it
COPY requirements.txt .

# Install the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

CMD ["python","server.py"]