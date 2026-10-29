from os import getenv
import threading
import time
from app import app as flask_app
from selenium import webdriver
import requests

BASE_URL = getenv('BASE_URL', 'http://127.0.0.1:5000')


def before_all(context):
    """Executed once before all tests"""
    context.base_url = BASE_URL
    WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))
    context.wait_seconds = WAIT_SECONDS

    context.server_thread = threading.Thread(
        target=flask_app.run,
        kwargs={'host': '0.0.0.0', 'port': 5000}
    )
    context.server_thread.daemon = True
    context.server_thread.start()
    time.sleep(5)
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    context.driver = webdriver.Chrome(options=options)
    requests.post(f"{context.base_url}/pets/reset")

def after_all(context):
    """Executed after all tests"""
    context.driver.quit()
    requests.get(f"{context.base_url}/shutdown")

def before_scenario(context, scenario):
    """Enable continuing execution after step failure if tagged."""
    if "continue_after_failed_step" in scenario.effective_tags:
        scenario.continue_after_failed_step = True