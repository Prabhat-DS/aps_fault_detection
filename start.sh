#!bin/sh
nohup airflow scheduler &
airflow webserver


# to start the docker(airflow) we need some command, for that we write some script start.sh
# hear we first lonch airflow scheduler and then webserver, webserver is going to give us an aplication(UI)
# sh is shell scrip