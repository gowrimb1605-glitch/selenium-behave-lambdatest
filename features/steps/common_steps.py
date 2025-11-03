\
import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground"

def _click_link_by_text(driver, text):
    driver.find_element(By.LINK_TEXT, text).click()

@given("I open the Selenium Playground")
def open_playground(context):
    context.driver.get(PLAYGROUND_URL)
    WebDriverWait(context.driver, 15).until(
        EC.title_contains("Selenium Playground")
    )

@when('I click "{link_text}"')
def click_link(context, link_text):
    _click_link_by_text(context.driver, link_text)

@then('the URL should contain "{fragment}"')
def url_contains(context, fragment):
    WebDriverWait(context.driver, 10).until(
        EC.url_contains(fragment)
    )
    assert fragment in context.driver.current_url

@when('I enter the message "{message}"')
def enter_message(context, message):
    # id + css used here
    input_box = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#user-message"))
    )
    input_box.clear()
    input_box.send_keys(message)
    context._message = message

@when('I click the button "Get Checked Value"')
def click_get_value(context):
    # xpath used here
    btn = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Get Checked Value')]"))
    )
    btn.click()

@then('I should see "{expected}" under "Your Message:"')
def verify_echo(context, expected):
    actual = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p#message"))
    ).text.strip()
    assert actual == expected, f"Expected '{expected}', got '{actual}'"

@when('I move the "Default value 15" slider to 95')
def move_slider(context):
    WebDriverWait(context.driver, 10).until(
        EC.title_contains("Drag & Drop")
    )
    # Locate the correct slider block by label text, then find input[type=range]
    block = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h4[contains(.,'Default value 15')]/following-sibling::div"))
    )
    slider = block.find_element(By.CSS_SELECTOR, "input[type='range']")
    value_label = block.find_element(By.CSS_SELECTOR, "output")
    # Drag until value is 95 (fallback loop in case of browser differences)
    actions = ActionChains(context.driver)
    # heuristic: move right several times
    for _ in range(25):
        actions.click_and_hold(slider).move_by_offset(10, 0).release().perform()
        if value_label.text.strip() == "95":
            break
    # ensure it's 95 (if not exact, nudge)
    while value_label.text.strip() != "95":
        actions.click_and_hold(slider).move_by_offset(2, 0).release().perform()
        if value_label.text.strip() == "95":
            break
    context._slider_value = value_label.text.strip()

@then("the slider value should be 95")
def assert_slider_value(context):
    assert context._slider_value == "95"

@when("I submit the form without data")
def submit_empty(context):
    WebDriverWait(context.driver, 10).until(
        EC.title_contains("Input Form Submit")
    )
    submit_btn = context.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

@then('I should see the HTML5 validation message "Please fill out this field."')
def assert_html5_msg(context):
    # Find the first required input and read its validationMessage
    required = context.driver.find_element(By.NAME, "name")
    msg = required.get_attribute("validationMessage")
    assert "Please fill out this field." in msg

@when("I fill the input form with valid data")
def fill_form(context):
    d = context.driver
    WebDriverWait(d, 10).until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )
    d.find_element(By.NAME, "name").send_keys("John Tester")
    d.find_element(By.NAME, "email").send_keys("john.tester@example.com")
    d.find_element(By.NAME, "password").send_keys("Str0ngPass!")
    d.find_element(By.NAME, "company").send_keys("Acme Inc.")
    d.find_element(By.NAME, "website").send_keys("https://example.com")
    Select(d.find_element(By.NAME, "country")).select_by_visible_text("United States")
    d.find_element(By.NAME, "city").send_keys("New York")
    d.find_element(By.NAME, "address_line1").send_keys("123 Test St")
    d.find_element(By.NAME, "address_line2").send_keys("Suite 456")
    d.find_element(By.NAME, "state").send_keys("NY")
    d.find_element(By.NAME, "zip").send_keys("10001")

@when("I submit the form")
def submit_form(context):
    context.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

@then('I should see the success message "Thanks for contacting us, we will get back to you shortly."')
def assert_success(context):
    alert = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.success-msg"))
    )
    assert "Thanks for contacting us, we will get back to you shortly." in alert.text.strip()
