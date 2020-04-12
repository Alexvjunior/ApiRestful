#publicly available docker image "python" on docker hub will be pulled
FROM python

#copying app.py from local directory to container's app folder
#creating directory app in container (linux machine)
ADD ./ /app
WORKDIR /app

#Install packages necessary 
RUN pip install -r requirements.txt

EXPOSE 5000

#running app.py in container
CMD python /app/app.py