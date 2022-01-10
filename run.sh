python3 -m venv ingestion_server
source ingestion_server/bin/activate

pip3 install -r requirements.txt
echo "Starting flask server"

gunicorn --bind 0.0.0.0:8000 run:app
