ECHO "Checking Python requirements"
python -m pip install -r config\requirements.txt

ECHO "Requirements met, running Python script"
python podcast_scraper.py

ECHO "Complete."
