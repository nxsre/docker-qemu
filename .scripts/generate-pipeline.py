#!/usr/bin/env python3
"""
generate-pipeline.py

generates a pipeline yaml file based on `pipeline.yml.j2`
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
        'comma separated list of target platforms: linux/amd64,linux/arm64/v8,linux/arm/v7,linux/arm/v6,linux/386'
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
    if '-rc' in version:
        versions[version]['rc'] = True
    elif int(''.join(version.split('.'))) > int(''.join(latest.split('.'))):
        latest = version

platforms = {
    'linux/amd64': {
        'short_name': 'amd64',
        'build-arg': 'opts=GOARCH=amd64',
    },
    'linux/arm64/v8': {
        'short_name': 'arm64',
        'build-arg': 'opts=GOARCH=arm64',
    },
    'linux/arm/v7': {
        'short_name': 'armv7',
        'build-arg': 'opts=GOARCH=arm GOARM=7',
    },
    'linux/arm/v6': {
        'short_name': 'armv6',
        'build-arg': 'opts=GOARCH=arm GOARM=6',
    },
    'linux/386': {
        'short_name': '386',
        'build-arg': 'opts=GOARCH=386',
    },
}

enabled_platforms = []

target_platforms = args.target_platform.split(',')

for target_platform in target_platforms:
    enabled_platforms.append({
        'long_name': target_platform,
        'short_name': platforms[target_platform]['short_name'],
        'build-arg': platforms[target_platform]['build-arg'],
    })

versions[latest]['latest'] = True

print(Template(args.template_file.read()).render(
    versions=versions,
    enabled_platforms=enabled_platforms,
    args_target_platforms=args.target_platform
))
