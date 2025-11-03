Feature: Simple Form Demo
  As a tester
  I want to verify the simple form demo
  So that user-entered text is echoed correctly

  Scenario: Echo typed text
    Given I open the Selenium Playground
    When I click "Simple Form Demo"
    Then the URL should contain "simple-form-demo"
    When I enter the message "Welcome to LambdaTest"
    And I click "Get Checked Value"
    Then I should see "Welcome to LambdaTest" under "Your Message:"
