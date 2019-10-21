FROM python:3.8.0-alpine

WORKDIR /crawler

COPY . .

RUN pip3 install -r requirements.txt && \
    chmod ug+x ./linux_launch.sh && \
    mkdir /output

VOLUME [ "/output" ]

ENTRYPOINT [ "./linux_launch.sh" ]
