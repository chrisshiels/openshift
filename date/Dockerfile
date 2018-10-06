from centos:7

expose 4000

run mkdir /app

workdir /app

copy date.py requirements.txt ./

run yum -y install python-virtualenv

run virtualenv /app/virtualenv

run /app/virtualenv/bin/pip install -r /app/requirements.txt

cmd /app/virtualenv/bin/gunicorn --workers 4 --bind 0.0.0.0:4000 date:app
