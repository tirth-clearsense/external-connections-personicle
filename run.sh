pip install -r requirements.txt
echo "Starting flask server"
gunicorn --bind 0.0.0.0:8000 run:app
