#!/bin/bash

# Make Sure to change the relevant repo and suffix
gitRepo="refLightModule"
suffix="/firmware/xu4Mqtt"

# Prefix is always kept constant for Mints Projects
prefix="/home/teamlary/gitHubRepos/"

repoPath="$prefix$gitRepo$suffix"

# m h  dom mon dow   command

cd "$repoPath" && sudo ./sudoRun.sh


