from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions

from utilities.capabilities import build_caps, hub_url
from behave import fixture, use_fixture

def _make_options(caps):
    browser = caps["browserName"].lower()
    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "edge":
        options = EdgeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    elif browser == "safari":
        options = SafariOptions()
    else:
        options = ChromeOptions()

    # Selenium 4 style: put everything on options
    options.set_capability("platformName", caps["platformName"])
    options.set_capability("browserVersion", caps["browserVersion"])
    options.set_capability("LT:Options", caps["LT:Options"])
    return options

@fixture
def selenium_browser(context, name):
    caps = build_caps(name)
    options = _make_options(caps)
    context.driver = webdriver.Remote(
        command_executor=hub_url(),
        options=options
    )
    try:
        context.driver.maximize_window()
    except Exception:
        pass
    yield context.driver
    try:
        context.driver.quit()
    except Exception:
        pass

def before_scenario(context, scenario):
    test_name = f"Selenium 101 — {scenario.feature.name} — {scenario.name}"
    use_fixture(selenium_browser, context, test_name)

def after_step(context, step):
    if step.status == "failed":
        try:
            context.driver.save_screenshot(f"screenshot_{step.name}.png")
        except Exception:
            pass
