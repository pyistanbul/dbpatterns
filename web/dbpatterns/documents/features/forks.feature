Feature: Forking created patterns
  Users can fork already created patterns.

  Scenario: Show fork form
    Given I am logged in as user "tester"
    And there is a pattern that named "Products"
    When go to the that pattern
    And click to fork button
    And the page should contains a form with "title" field

  Scenario: Forking action
    Given I am logged in as user "tester"
    And there is a pattern that named "Categories"
    When fork the that pattern as "Forked Categories"
    Then the redirected page should contains "Forked Categories"
    And when click to show button
    Then the page should contains "fork-of"