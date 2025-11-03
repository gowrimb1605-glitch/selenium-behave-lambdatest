Feature: Drag & Drop Sliders
  As a tester
  I want to set slider values
  So that the default slider reads 95

  Scenario: Set default slider to 95
    Given I open the Selenium Playground
    When I click "Drag & Drop Sliders"
    And I move the "Default value 15" slider to 95
    Then the slider value should be 95
