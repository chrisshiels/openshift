from centos:7

expose 4000

run mkdir /app

workdir /app

run yum -y install python-virtualenv

copy requirements.txt ./

run virtualenv /app/virtualenv && \
    /app/virtualenv/bin/pip install -r /app/requirements.txt

copy date.py ./

cmd /app/virtualenv/bin/gunicorn --workers 4 --bind 0.0.0.0:4000 date:app
