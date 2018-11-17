# date

    host$ # Setup virtualenv.
    host$ virtualenv virtualenv
    host$ . virtualenv/bin/activate
    (virtualenv) host$ pip install -r requirements.txt


    (virtualenv) host$ # Run tests.
    (virtualenv) host$ pytest -v


    (virtualenv) host$ # Run with 'flask run'.
    (virtualenv) host$ FLASK_APP=date.py FLASK_ENV=development \
        flask run --port 4000 &
    (virtualenv) host$ curl http://localhost:4000/date
    (virtualenv) host$ kill %


    (virtualenv) host$ # Run with 'gunicorn'.
    (virtualenv) host$ gunicorn --workers 4 --bind 127.0.0.1:4000 date:app &
    (virtualenv) host$ curl http://localhost:4000/date
    (virtualenv) host$ kill %


    (virtualenv) host$ # Build and run Docker image.
    (virtualenv) host$ docker build -t date:0.0.1 .
    (virtualenv) host$ docker run \
        --rm \
        --name date.docker \
        -d \
        -p 4000:4000 \
        date:0.0.1
    (virtualenv) host$ curl http://localhost:4000/date
    (virtualenv) host$ docker rm -f date.docker


    (virtualenv) host$ # Start registry.
    (virtualenv) host$ docker run \
        --name registry \
        -d \
        -p 5000:5000 \
        --restart=always \
        registry:2


    (virtualenv) host$ # Push to registry.
    (virtualenv) host$ docker tag date:0.0.1 localhost:5000/date:0.0.1
    (virtualenv) host$ docker push localhost:5000/date:0.0.1


## OpenShift - ...

    host$ oc login -u developer

    host$ oc new-project project1
    host$ oc new-app localhost:5000/date:0.0.1 \
        --name date --insecure-registry
    ..
    --> Creating resources ...
        imagestream.image.openshift.io "date" created
        deploymentconfig.apps.openshift.io "date" created
        service "date" created
    ..

    host$ oc get imagestream
    NAME      DOCKER REPO                     TAGS      UPDATED
    date      172.30.1.1:5000/project1/date   0.0.1     13 seconds ago
    host$ oc get imagestreamtag
    NAME         DOCKER REF                                                                                    UPDATED
    date:0.0.1   localhost:5000/date@sha256:82f660dd932dbd0094427f99afc13e0da717d734159fc431c651acc2f66fe7a6   15 seconds ago

    host$ oc scale dc date --replicas 3

    host$ oc expose service date
    host$ curl http://date-project1.127.0.0.1.nip.io/date


## OpenShift - ...

    host$ oc new-project project2
    host$ oc import-image localhost:5000/date:0.0.1 --insecure --confirm

    host$ oc get imagestream
    NAME      DOCKER REPO                     TAGS      UPDATED
    date      172.30.1.1:5000/project2/date   0.0.1     About a minute ago
    host$ oc get imagestreamtag
    NAME         DOCKER REF                                                                                    UPDATED
    date:0.0.1   localhost:5000/date@sha256:82f660dd932dbd0094427f99afc13e0da717d734159fc431c651acc2f66fe7a6   About a minute ago


## OpenShift - ...

    host$ oc --context default/127-0-0-1:8443/system:admin -n default \
            get service docker-registry
    NAME              TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
    docker-registry   ClusterIP   172.30.1.1   <none>        5000/TCP   20h

    host$ oc new-project project3
    host$ oc whoami -c
    project3/127-0-0-1:8443/developer

    host$ oc whoami -t | \
            docker login -u developer --password-stdin 172.30.1.1:5000

    host$ docker tag date:0.0.1 172.30.1.1:5000/project3/date:0.0.1
    host$ docker push 172.30.1.1:5000/project3/date:0.0.1

    host$ oc get imagestream
    NAME      DOCKER REPO                     TAGS      UPDATED
    date      172.30.1.1:5000/project3/date   0.0.1     About a minute ago
    host$ oc get imagestreamtag
    NAME         DOCKER REF                                                                                              UPDATED
    date:0.0.1   172.30.1.1:5000/project3/date@sha256:82f660dd932dbd0094427f99afc13e0da717d734159fc431c651acc2f66fe7a6   About a minute ago


## OpenShift - ...

    host$ oc new-project project4
    host$ oc new-app \
            https://github.com/chrisshiels/openshift.git#feature/date \
            --name date \
            --strategy docker \
            --context-dir date

    ..
    --> Creating resources ...
        imagestream.image.openshift.io "centos" created
        imagestream.image.openshift.io "date" created
        buildconfig.build.openshift.io "date" created
        deploymentconfig.apps.openshift.io "date" created
        service "date" created
    ..

    host$ oc logs -f date-1-build

    host$ oc get imagestream
    NAME      DOCKER REPO                       TAGS      UPDATED
    centos    172.30.1.1:5000/project4/centos   7         4 minutes ago
    date      172.30.1.1:5000/project4/date     latest    2 minutes ago
    host$ oc get imagestreamtag
    NAME          DOCKER REF                                                                                              UPDATED
    centos:7      centos@sha256:dc29e2bcceac52af0f01300402f5e756cc8c44a310867f6b94f5f7271d4f3fec                          4 minutes ago
    date:latest   172.30.1.1:5000/project4/date@sha256:674e6e9b0c4461a766be25a701c6ed784f4c258d1190921862bf593a9174afb7   2 minutes ago

    host$ oc scale dc date --replicas 3

    host$ oc expose service date
    host$ curl http://date-project1.127.0.0.1.nip.io/date

    host$ oc start-build date
