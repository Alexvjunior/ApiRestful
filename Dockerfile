#publicly available docker image "python" on docker hub will be pulled
FROM python

#creating directory helloworld in container (linux machine)
RUN mkdir c:\home\spider

#copying helloworld.py from local directory to container's helloworld folder
COPY spider.py /home/spider/spider.py
COPY parser.py /home/spider/parser.py
COPY emailPromo.py /home/spider/emailPromo.py
COPY template.html /home/spider/template.html

#Install packages necessary 
RUN pip install requests
RUN pip install bs4
RUN pip install lxml

#running spider.py in container
CMD python /home/spider/spider.py