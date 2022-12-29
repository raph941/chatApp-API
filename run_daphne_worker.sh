
# Run the daphne web service
daphne SocialProject.asgi:application --port $PORT --bind 0.0.0.0

# Run the worker
python manage.py runworker