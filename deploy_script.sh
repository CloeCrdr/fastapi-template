#!/bin/bash

# Aller dans le répertoire de l'application
cd /home/ec2-user/fastapi_template

# Pull les dernières modifications du dépôt
git pull origin main

# Installer les dépendances
pip install -r requirements.txt

# Redémarrer le service (ajustez selon votre configuration)
sudo systemctl restart nginx
