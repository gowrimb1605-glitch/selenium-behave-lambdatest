\
import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground"
DRAG_URL = f"{PLAYGROUND_URL}/drag-drop-sliders"

def _click_link_by_text(driver, text):
    driver.find_element(By.LINK_TEXT, text).click()
    
@given("I open the Selenium Playground")
def open_playground(context):
    context.driver.get(PLAYGROUND_URL)

    # Be tolerant of redirects/slow loads on cloud browsers
    WebDriverWait(context.driver, 30).until(
        EC.url_contains("selenium-playground")
    )

    # Wait for a reliable element on the page (link in the left panel)
    WebDriverWait(context.driver, 30).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Simple Form Demo"))
    )

@when('I click "{link_text}"')
def click_link(context, link_text):
    WebDriverWait(context.driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, link_text))
    ).click()


@then('the URL should contain "{fragment}"')
def url_contains(context, fragment):
    WebDriverWait(context.driver, 10).until(
        EC.url_contains(fragment)
    )
    assert fragment in context.driver.current_url

@when('I enter the message "{message}"')
def enter_message(context, message):
  
    input_box = context.driver.find_element(By.XPATH,"//input[@placeholder='Please enter your Message']")
    input_box.clear()
    input_box.send_keys(message)
    context._message = message

@when('I click the button "Get Checked Value"')
def click_get_value(context):
    # xpath used here
    btn = context.driver.find_element(By.XPATH,"//button[text()='Get Checked Value']")

    btn.click()

@then('I should see "{expected}" under "Your Message:"')
def verify_echo(context, expected):
    actual = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH,"//p[@id='message']"))
    ).text.strip()
    assert actual == expected, f"Expected '{expected}', got '{actual}'"

@when('I move the "Default value 15" slider to 95')
def move_slider(context):
    # If click didn't navigate, force navigation to the sliders page
    if "drag-drop-sliders" not in context.driver.current_url:
        try:
            context.driver.get(DRAG_URL)
        except Exception:
            pass

    # If a new tab/window opened, switch to it
    try:
        handles = context.driver.window_handles
        if len(handles) > 1:
            context.driver.switch_to.window(handles[-1])
    except Exception:
        pass

    # Wait for the specific slider section to be visible (element-based, not URL-based)
    block = WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h4[contains(.,'Default value 15')]/following-sibling::div")
        )
    )

    slider = block.find_element(By.CSS_SELECTOR, "input[type='range']")
    value_label = block.find_element(By.CSS_SELECTOR, "output")

    # Drag until the label shows 95 (simple heuristic for cloud)
    actions = ActionChains(context.driver)
    for _ in range(30):
        actions.click_and_hold(slider).move_by_offset(8, 0).release().perform()
        if value_label.text.strip() == "95":
            break

    # (Optional) small nudges if not exact
    tries = 0
    while value_label.text.strip() != "95" and tries < 10:
        actions.click_and_hold(slider).move_by_offset(2, 0).release().perform()
        tries += 1

    context._slider_value = value_label.text.strip()


@then("the slider value should be 95")
def assert_slider_value(context):
    assert context._slider_value == "95"

@when("I submit the form without data")
def submit_empty(context):
    WebDriverWait(context.driver, 30).until(
        EC.url_contains("input-form-demo")
    )
    submit_btn = WebDriverWait(context.driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "(//button[@type='submit'])[2]"))
)
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
        EC.visibility_of_element_located((By.XPATH, "//input[@name='name']"))
    )

    d.find_element(By.XPATH, "//input[@name='name']").send_keys("John Tester")
    d.find_element(By.XPATH, "(//input[@name='email'])[2]").send_keys("john.tester@example.com")
    d.find_element(By.XPATH, "//input[@name='password']").send_keys("Str0ngPass!")
    d.find_element(By.XPATH, "//input[@name='company']").send_keys("Acme Inc.")
    d.find_element(By.XPATH, "//input[@name='website']").send_keys("https://example.com")

    # Dropdown for Country
    country_dropdown = d.find_element(By.XPATH, "//select[@name='country']")
    Select(country_dropdown).select_by_visible_text("United States")

    d.find_element(By.XPATH, "//input[@name='city']").send_keys("New York")
    d.find_element(By.XPATH, "//input[@name='address_line1']").send_keys("123 Test St")
    d.find_element(By.XPATH, "//input[@name='address_line2']").send_keys("Suite 456")
    d.find_element(By.XPATH, "//input[@id='inputState']").send_keys("NY")
    d.find_element(By.XPATH, "//input[@name='zip']").send_keys("10001")


@when("I submit the form")
def submit_form(context):
    context.driver.find_element(By.XPATH, "(//button[@type='submit'])[2]").click()

@then('I should see the success message "Thanks for contacting us, we will get back to you shortly."')
def assert_success(context):
    alert = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.success-msg"))
    )
    assert "Thanks for contacting us, we will get back to you shortly." in alert.text.strip()
