from datetime import datetime
import os

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'voicegenie')

# Slack Configuration
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#kpi-updates')

# Date Format
DATE_FORMAT = "%Y-%m-%d"