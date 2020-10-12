# python version
FROM python:3.6-alpine
WORKDIR /home/raphael/chatAppContainer
COPY ./requirements.txt ./Pipfile /home/raphael/chatAppContainer/

# Set encoding
ENV LC_ALL="en_US.utf8"
ENV LANG="en_US.utf8"
ENV PYTHONUNBUFFERED 1
#prevent python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# install dependencies
RUN apk update && \
    apk add --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    git bash
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev
    
RUN pip install -r requirements.txt

# copy project from current directory to Workdir
COPY . .

# run entrypoint.sh
# ENTRYPOINT ["./entrypoint.sh"]