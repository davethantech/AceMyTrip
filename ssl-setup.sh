#!/bin/bash
DOMAIN=your-domain.com
EMAIL=your-email@example.com

# Start Nginx only (to serve ACME challenge)
docker-compose -f docker-compose.prod.yml up -d nginx

# Request Let's Encrypt certificate
docker-compose -f docker-compose.prod.yml run --rm certbot certonly --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Restart everything with SSL
docker-compose -f docker-compose.prod.yml up -d --build
