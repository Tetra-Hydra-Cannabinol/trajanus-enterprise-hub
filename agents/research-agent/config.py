"""
Configuration for Research Agent
Loads environment variables and defines settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from credentials file
CREDENTIALS_PATH = "G:/My Drive/00 - Trajanus USA/12-Credentials.env"
load_dotenv(CREDENTIALS_PATH)

# API Keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Directories
OUTPUT_DIR = "G:/My Drive/00 - Trajanus USA/00-Command-Center/Daily-Briefings"
DOWNLOAD_DIR = "G:/My Drive/00 - Trajanus USA/07-Traffic-Engineering"
LOG_DIR = "G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/research-agent/logs"

# Schedule
RUN_TIME = "05:00"

# YouTube search queries (rotated daily)
YOUTUBE_QUERIES = [
    "Claude AI tips 2025",
    "Claude Code tutorial",
    "AI coding workflow",
    "prompt engineering Claude",
    "AI agent development"
]

# Document hunter target URLs
DOT_URLS = {
    "florida": [
        "https://www.fdot.gov/planning/systems/programs/sm/accman",
        "https://www.fdot.gov/traffic/trafficservices/studies"
    ],
    "georgia": [
        "https://www.dot.ga.gov/PartnerSmart/DesignManuals",
        "https://www.dot.ga.gov/GDOT/pages/TrafficData.aspx"
    ],
    "texas": [
        "https://www.txdot.gov/business/resources/traffic-analysis.html",
        "https://www.txdot.gov/business/resources/roadway-design.html"
    ]
}

def validate_config():
    """Check if required config values are present"""
    missing = []
    if not YOUTUBE_API_KEY:
        missing.append("YOUTUBE_API_KEY")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not SUPABASE_URL:
        missing.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        missing.append("SUPABASE_KEY")
    return missing

if __name__ == "__main__":
    missing = validate_config()
    if missing:
        print(f"Missing environment variables: {missing}")
    else:
        print("All configuration loaded successfully")
