# Copyright 2024 Vladimir Ignatev <ya.na.pochte@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Portions of this software are based on work by Google, Inc.
# Copyright 2020 Google, Inc. Licensed under the Apache License, Version 2.0.

# Use the official Python image.
# https://hub.docker.com/_/python
FROM --platform=linux/amd64 python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=True

# Install system dependencies
RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir \
    Flask==3.0.3 \
    gunicorn==22.0.0 \
    Werkzeug==3.0.3 \
    geoip2==4.8.0 \
    maxminddb==2.6.2

ENV APP_HOME=/app
WORKDIR $APP_HOME

# Download GeoLite2 databases
RUN curl -fsL --retry 5 -o "GeoLite2-Country.mmdb" "https://git.io/GeoLite2-Country.mmdb"
RUN curl -fsL --retry 5 -o "GeoLite2-ASN.mmdb" "https://git.io/GeoLite2-ASN.mmdb"

# Copy local code to the container image.
COPY . ./

# Install production dependencies.
# RUN pip install --no-cache-dir -r requirements.txt


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

CMD sh -c "gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app"
