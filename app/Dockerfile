FROM quay.io/ukhomeofficedigital/centos-base:v0.5.12

ENV USERMAP_UID 1000
ENV PYTHONPATH="$PYTHONPATH:/scanner"

# Setup folder structure and copy files
RUN mkdir -p \
             /tmp/scanner/scripts \
             /tmp/scanner/data/nats \
             /tmp/scanner/stage/nats \
             /tmp/scanner/quarantine/nats \
             /tmp/scanner/failed_to_parse/nats \
             /tmp/scanner/log \
             /tmp/scanner/bin \
             /scanner \
             /home/runner/.pm2 \
             /home/runner/.ssh

COPY packages.txt /tmp/scanner/scripts
COPY ecosystem.config.js /tmp/scanner/scripts
COPY docker-entrypoint.sh /
ADD bin /tmp/scanner/bin
ADD scripts /tmp/scanner/scripts

# Add user
RUN groupadd -r runner && \
    useradd --no-log-init -u $USERMAP_UID -r -g runner runner && \
    groupadd docker && \
    usermod -aG docker runner && \
    chown -R runner:runner /scanner && \
    chown -R runner:runner /home/runner/.pm2 && \
    chown -R runner:runner /home/runner/.ssh

# Install script dependencies
RUN yum update -y
RUN yum install -y wget make gcc openssl-devel zlib-devel pcre-devel bzip2-devel libffi-devel epel-release

# Install Python3.7.2 and pip modules
RUN cd /usr/bin && \
    wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz && \
    tar xzf Python-3.7.2.tgz && \
    cd Python-3.7.2 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    alternatives --install /usr/bin/python python /usr/local/bin/python3.7 1
RUN python -m pip install --no-cache-dir -r /tmp/scanner/scripts/packages.txt

# Fix yum installer with Python3.7 running as a global default
RUN sed -i '/#!\/usr\/bin\/python/c\#!\/usr\/bin\/python2.7' /usr/bin/yum && \
    sed -i '/#! \/usr\/bin\/python/c\#! \/usr\/bin\/python2.7' /usr/libexec/urlgrabber-ext-down

# Install PM2
RUN curl -sL https://raw.githubusercontent.com/nodesource/distributions/master/rpm/setup_11.x -o setup_11.x && bash setup_11.x && rm setup_11.x && \
    yum install -y nodejs && \
    npm install -g pm2

VOLUME ["/scanner"]
RUN chown -R runner:runner /scanner

RUN chown runner:runner /docker-entrypoint.sh && \
chmod +x /docker-entrypoint.sh

USER ${USERMAP_UID}

WORKDIR /scanner

ENTRYPOINT ["/docker-entrypoint.sh"]

# Start PM2
CMD pm2-docker /scanner/scripts/ecosystem.config.js  -- --config $S3_BUCKET_NAME \
    $S3_KEY_PREFIX $S3_ACCESS_KEY_ID $S3_SECRET_ACCESS_KEY \
    $CLAMAV_URL $CLAMAV_PORT \
    $INPUT_DIR $OUTPUT_DIR $QUARANTINE_DIR

# Save PM2 configuration
RUN pm2 save
