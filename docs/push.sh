#!/bin/sh
cd ~/python/esp8266-upy/docs
git add indexes/*.md
git add _static/_*.md
git add ../readme.md
git add ../readme_ENG.md
git add drivers.json
git commit -m "update Readme and indexes"
echo "Changes commited/pushed into local Git :-)"
echo "GIT PUSH must still be performed!"
