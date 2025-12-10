#!/bin/bash
python manage.py loaddata fixtures/sample_users.json
python manage.py loaddata fixtures/sample_products.json
