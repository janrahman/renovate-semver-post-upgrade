# Semver post upgrade for Renovate

A small script to increase the minor patch or add a defined description to `semver.txt`.
It should run after a Renovate dependency update.
This tool is written for my dev team at work.

## Getting started

```sh
python3 semver_post_upgrade.py
```

The script checks the content of the existing `semver.txt` and prepend a new semver or add the description below the version tag.

### Initial Configuration

The following setup is required:

* Python >= 3.8
* `semver.txt` on root dir of the git project scanned by Renovate
* a scheduled Renovate job (Github actions, Bamboo, ...)

## Developing

Just edit the python script for your purpose.
Use ruff (with default settings) to lint and format the script file.

### Publishing

Add the script to the renovate configs and allow to use the script as a postcommand.

## Configuration

An example how to setup this script for Renovate:

```json
{
  "allowedPostUpgradeCommands": ["^python3 semver_post_upgrade.py$"],
  "postUpgradeTasks": {
    "commands": ["python3 semver_post_upgrade.py"],
    "fileFilters": ["semver.txt"],
    "executionMode": "branch"
  }
}
```

## Features

* prepend new version and description if Release or Hotfix description is matched
* always increase minor version
* add description to latest changelog

## Links

* <https://github.com/renovatebot/renovate>
* <https://github.com/astral-sh/ruff>
