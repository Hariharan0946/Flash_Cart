web: gunicorn flashcart.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 2
worker: celery -A flashcart worker -l info -Q default
beat: celery -A flashcart beat -l info
