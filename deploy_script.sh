#!/bin/bash

cd /home/ec2-user/fastapi_template

git pull origin main

pip install -r requirements.txt

sudo systemctl restart nginx
