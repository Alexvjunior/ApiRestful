#publicly available docker image "python" on docker hub will be pulled
FROM python

#copying spider.py from local directory to container's helloworld folder
#creating directory helloworld in container (linux machine)
ADD ./ /crawler
WORKDIR /crawler

#Install packages necessary 
RUN pip install -r requirements.txt

#running spider.py in container
CMD python /crawler/app.py