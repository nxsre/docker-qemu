#!/usr/bin/env python
"""
generate-pipeline.py

generates a pipeline yaml file based on `generated-pipeline.yml.j2`
"""

import argparse
import json
from jinja2 import Template

parser = argparse.ArgumentParser(description='Generate pipeline file for docker-qemu')

parser.add_argument(
    '-t',
    '--template-file',
    default=".scripts/pipeline.yml.j2",
    type=argparse.FileType('r'),
    dest="template_file"
)
parser.add_argument(
    '-v',
    '--versions-file',
    default="versions.json",
    type=argparse.FileType('r'),
    dest="versions_file"
)

args = parser.parse_args()

with args.versions_file as stored_versions:
    versions = json.load(stored_versions)

latest = "0.0"

for version in versions:
    version_list = versions[version]['version'].split('.')
    versions[version]['major'] = version_list[0]
    versions[version]['minor'] = version_list[1]
    versions[version]['patch'] = version_list[2]
    if int(''.join(version.split('.'))) > int(''.join(latest.split('.'))):
        latest = version

versions[latest]['latest'] = True

template = Template(args.template_file.read()).render(versions=versions)

print(template)
