import os
from dotenv import load_dotenv
load_dotenv()

LT_USERNAME = os.getenv("LT_USERNAME")
LT_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")

def build_caps(test_name: str):
    platform = os.getenv("LT_PLATFORM", "Windows 10")
    browser = os.getenv("LT_BROWSER", "Chrome")
    version = os.getenv("LT_VERSION", "latest")

    lt_options = {
        "build": "Selenium 101 — Behave",
        "name": test_name,
        "selenium_version": "4.24.0",
        "network": True,
        "video": True,
        "console": "true",
        "visual": True,
        "w3c": True,
        "timezone": "UTC",
        "project": "Selenium 101",
        "idleTimeout": 120,
        "geoLocation": "GB",
    }

    # Return Selenium 4 style capability keys
    caps = {
        "platformName": platform,
        "browserName": browser,
        "browserVersion": version,
        "LT:Options": lt_options
    }
    return caps

def hub_url():
    if not LT_USERNAME or not LT_ACCESS_KEY:
        raise RuntimeError("LT_USERNAME / LT_ACCESS_KEY not set. Add them to .env or env vars.")
    return f"https://{LT_USERNAME}:{LT_ACCESS_KEY}@hub.lambdatest.com/wd/hub"
