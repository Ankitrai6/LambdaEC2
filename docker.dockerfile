FROM python:3.9

USER root

WORKDIR /main 

COPY . /main
 
RUN pip install -r requirements.txt 

EXPOSE 5000 

CMD ["python", "main.py"]
