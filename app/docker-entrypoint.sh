#!/bin/bash

# Copy all files and folders from the staging area to PVC
cp -R /tmp/scanner/data /scanner
cp -R /tmp/scanner/stage /scanner
cp -R /tmp/scanner/scripts /scanner
cp -R /tmp/scanner/quarantine /scanner
cp -R /tmp/scanner/log /scanner
cp -R /tmp/scanner/bin /scanner
cp -R /tmp/scanner/failed_to_parse /scanner

# Set permissions
chown -R runner:runner /scanner/data
chown -R runner:runner /scanner/stage
chown -R runner:runner /scanner/scripts
chown -R runner:runner /scanner/quarantine
chown -R runner:runner /scanner/log
chown -R runner:runner /scanner/bin
chown -R runner:runner /scanner/failed_to_parse

exec "$@"
