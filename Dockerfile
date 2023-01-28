# this file is ceated to make a docker image

# creating base image
FROM python:3.8 
# we make our self as root user 
USER root
# we creat a folder to copy our code in /app folder
RUN mkdir /app
# i want to copy every thing from this directry in /app folder
COPY . /app/
# next we will set working directory to /app location
WORKDIR /app/
RUN pip3 install -r requirements.txt

# we need to set some env veriable for airflow
# airflow home veriable where we will write the airflow code
ENV AIRFLOW_HOME="/app/airflow"
# how much time it shold hold airflow for loding  
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True

# initialise the data base in airflow
RUN airflow db init 
# we need to creat one user where will do airflow (-e:eamil id, -f: first name, -l:last name ,
# -p:Airflo password, -r:role, -u:user name)
RUN airflow users create  -e prabhat.18811@gmail.com -f Prabhat -l Kumar -p admin -r Admin  -u admin

# for the exicution of start.sh commond
RUN chmod 777 start.sh
# we are going to install aws command line interface(awscli)
RUN apt update -y && apt install awscli -y

# at last we need start script 
ENTRYPOINT [ "/bin/sh" ]
# whenever we run the docker, it will creat a container, and it will run the start.sh to start airflow
CMD ["start.sh"]
