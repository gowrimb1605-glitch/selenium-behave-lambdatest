from selenium import webdriver
from utilities.capabilities import build_caps, hub_url
from selenium.webdriver.remote.webdriver import WebDriver
from behave import fixture, use_fixture

@fixture
def selenium_browser(context, name):
    caps = build_caps(name)
    context.driver = webdriver.Remote(
        command_executor=hub_url(),
        options=webdriver.ChromeOptions() if caps["browserName"].lower()=="chrome" else None,
        desired_capabilities=caps
    )
    context.driver.maximize_window()
    yield context.driver
    try:
        context.driver.quit()
    except Exception:
        pass

def before_scenario(context, scenario):
    test_name = f"Selenium 101 — {scenario.feature.name} — {scenario.name}"
    use_fixture(selenium_browser, context, test_name)

def after_step(context, step):
    # Embed a screenshot on failure for quick debugging in LT
    if step.status == "failed":
        try:
            context.driver.save_screenshot(f"screenshot_{step.name}.png")
        except Exception:
            pass
