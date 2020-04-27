# we will get a light verion(alpine) of python, which include all essential python stuff and then will apply our docker image on it.
FROM python:3.7-alpine

ENV PYTHHONUNBUFFERED=1
# recommeded method
# setting python to unbuffered mode, i.e., python will immediately dump output instead of keeping it into buffer

# will dump dependcies from directory req. file to docker's req. file 
COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# create a app dir on docker image
RUN mkdir /app
# /app will be default dic, so any execution will take place from here, unless specified
WORKDIR /app

COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# we could add an user will only run access
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user