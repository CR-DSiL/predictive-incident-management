#!/bin/bash

#envsubst < ./config/config.yaml

function replaceEnvVars() {
	originalfile=$1
	tmpfile=$(mktemp)
	cp --attributes-only --preserve $originalfile $tmpfile
	cat $originalfile | envsubst > $tmpfile && mv $tmpfile $originalfile
}

replaceEnvVars "./config/config.yaml" #make sure to provide appropraite config file
replaceEnvVars "./data/login.txt"

exec "$@"