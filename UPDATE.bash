#!/bin/bash

set -e

git pull || exit 1
git add .
read -p "Enter commit message: " MESSAGE
git commit -m "$MESSAGE"
sleep 2
git push || exit 
echo "done"
