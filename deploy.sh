#!/bin/bash

python manage.py collectstatic -y 
python manage.py compress
git add . 
git commit -m 'latest'
git push origin master