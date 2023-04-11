#!/bin/sh

set -e

mkdir -p /kaniko/.docker

FILE='/kaniko/.docker/config.json'

export REGISTRIES=0

_add_registry() {
  REGISTRY="${1}"
  USERNAME="${2}"
  PASSWORD="${3}"
  if [ "$REGISTRIES" -gt 0 ]; then
    printf "%s" "," >> "${FILE}"
  fi
  cat <<xEOF >> "${FILE}"
    "${REGISTRY}": {
      "auth": "$(printf "%s:%s" "${USERNAME}" "${PASSWORD}" | base64 -w 0)"
    }
xEOF
  export REGISTRIES=$((REGISTRIES+1))
}



cat <<xEOF > "${FILE}"
{
  "auths": {
xEOF

# GitLab Registry
echo "Configuring ${CI_REGISTRY}"
# The values are always set, since we're running in gitlab
_add_registry "${CI_REGISTRY}" "${CI_REGISTRY_USER}" "${CI_REGISTRY_PASSWORD}"

# Docker Hub index.docker.io
if [ -n "${DOCKERHUB_USERNAME}" ]  && [ -n "${DOCKERHUB_PASSWORD}" ]; then
  echo "Configuring docker.io"
  _add_registry "https://index.docker.io/v1/" "${DOCKERHUB_USERNAME}" "${DOCKERHUB_PASSWORD}"
fi

cat <<xEOF >> "${FILE}"
  }
}
xEOF

if [ "${REGISTRIES}" -eq 0 ]; then
  echo "ERROR! No registries configured!"
  echo "You must configure one of the following variables sets:"
  echo "------"
  echo "DOCKERHUB_USERNAME DOCKERHUB_PASSWORD DOCKERHUB_REPO_NAME"
  echo "--or--"
  echo "GITHUB_USERNAME GITHUB_STATUS_TOKEN GITHUB_REPO_NAME"
  exit 1
fi

