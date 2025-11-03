Feature: Input Form Submit
  As a tester
  I want to verify form validation and submission
  So that proper errors and success are shown

  Scenario: Validation and successful submit
    Given I open the Selenium Playground
    When I click "Input Form Submit"
    And I submit the form without data
    Then I should see the HTML5 validation message "Please fill out this field."
    When I fill the input form with valid data
    And I submit the form
    Then I should see the success message "Thanks for contacting us, we will get back to you shortly."
