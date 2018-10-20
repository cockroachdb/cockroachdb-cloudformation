FROM ubuntu:16.04
ENV JAVA_TOOL_OPTIONS "-Dfile.encoding=UTF8"

# Install
RUN apt-get -y update; apt-get -y install openjdk-8-jdk maven ant git wget
RUN git clone https://github.com/robert-s-lee/oltpbench.git --branch cockroachdb --single-branch oltpbenchmark; cd oltpbenchmark; ant
RUN wget -qO- https://binaries.cockroachdb.com/cockroach-v2.0.6.linux-amd64.tgz | tar  xvz
RUN cp -i cockroach-v2.0.6.linux-amd64/cockroach /usr/local/bin

WORKDIR oltpbenchmark

ENTRYPOINT ["/bin/bash","./oltpbench.sh"]
