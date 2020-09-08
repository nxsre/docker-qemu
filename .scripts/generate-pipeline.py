#!/usr/bin/env python
"""
generate-pipeline.py

generates a pipeline yaml file based on `generated-pipeline.yml.j2`
"""

import argparse
import json
from jinja2 import Template

parser = argparse.ArgumentParser(description='Generate child pipelines file based on a jinja2 template')

parser.add_argument(
    '-p',
    '--target-platform',
    default="linux/amd64",
    dest="target_platform",
    help=(
        'comma separated list of target platforms: linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v6 '
        '(default: linux/amd64)'
    ),
)
parser.add_argument(
    '-t',
    '--template-file',
    default=".scripts/pipeline.yml.j2",
    type=argparse.FileType('r'),
    dest="template_file",
    help='(default: .scripts/pipeline.yml.j2)',
)
parser.add_argument(
    '-v',
    '--versions-file',
    default="versions.json",
    type=argparse.FileType('r'),
    dest="versions_file",
    help='(default: versions.json)',
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

template = Template(args.template_file.read()).render(versions=versions, target_platform=args.target_platform)

print(template)
