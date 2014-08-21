# DOCKER-VERSION 1.0.0
FROM debian:7.4

COPY . /tmp/build/
RUN (test -f /tmp/build/.dockerignore && for f in $(cat /tmp/build/.dockerignore); do rm -rf /tmp/build/$f; done) || true
RUN mkdir /build && cp -r /tmp/build / && chmod -R go+rX /build && rm -rf /tmp/build
RUN sh /build/provision.sh
RUN rm -r /build

USER autoguard
WORKDIR /app
CMD ["/app/venv/bin/autoguard", "start"]
EXPOSE 9000

