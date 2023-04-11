#!/usr/bin/env python3
"""
generate-manifests.py

generates a manifests yaml files based on `manifest.yml.j2`
"""

import argparse
import json
from jinja2 import Template

parser = argparse.ArgumentParser(description='Generate child pipelines file based on a jinja2 template')

parser.add_argument(
    '-c',
    '--current-version',
    default="7.2",
    dest="current_version",
    help=(
        'The current version of the build'
        '(default: 7.2)'
    ),
)
parser.add_argument(
    '-t',
    '--template-file',
    default=".scripts/manifest.yml.j2",
    type=argparse.FileType('r'),
    dest="template_file",
    help='(default: .scripts/manifest.yml.j2)',
)
parser.add_argument(
    '-v',
    '--versions-file',
    default="versions.json",
    type=argparse.FileType('r'),
    dest="versions_file",
    help='(default: versions.json)',
)
parser.add_argument(
    '-e',
    '--enabled-platforms',
    default="linux/amd64,linux/arm64/v8,linux/arm/v7,linux/386",
    dest="enabled_platforms",
    help='(default: linux/amd64,linux/arm64/v8,linux/arm/v7,linux/386)',
)
parser.add_argument(
    '-i',
    '--image',
    default="ixdotai/qemu",
    dest="image",
    help='(default: ixdotai/qemu)',
)
args = parser.parse_args()

with args.versions_file as stored_versions:
    enabled_versions = json.load(stored_versions)

latest = "0.0"
version = {'current': args.current_version, 'latest': False}

for enabled_version in enabled_versions:
    if (not '-rc' in enabled_version) and (int(''.join(enabled_version.split('.'))) > int(''.join(latest.split('.')))):
        latest = str(enabled_version)

if latest == args.current_version:
    version['latest'] = True

#for enabled_version in enabled_versions:
#    if current_version ==

available_platforms = {
    'linux/amd64': {
        'architecture': 'amd64',
        'os': 'linux',
        'variant': False,
    },
    'linux/arm64/v8': {
        'architecture': 'arm64',
        'os': 'linux',
        'variant': 'v8',
    },
    'linux/arm/v7': {
        'architecture': 'arm',
        'os': 'linux',
        'variant': 'v7',
        'tag-variant': True,
    },
    'linux/arm/v6': {
        'architecture': 'arm',
        'os': 'linux',
        'variant': 'v6',
        'tag-variant': True,
    },
    'linux/386': {
        'architecture': '386',
        'os': 'linux',
        'variant': False,
    },
}

platforms = []
enabled_platforms = args.enabled_platforms.split(',')

for platform in enabled_platforms:
    platforms.append({
        'name': platform,
        'architecture': available_platforms[platform]['architecture'],
        'os': available_platforms[platform]['os'],
        'variant': available_platforms[platform]['variant'],
    })

print(Template(args.template_file.read()).render(version=version, platforms=platforms, image=args.image))
