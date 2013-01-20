Feature: Forking created patterns
  Users can fork already created patterns.

  Background:
    Given I am logged in as user "tester"
    And there is a pattern that named "Products"
    When I am logged out
    And I am logged in as user "tester-2"


  Scenario: Show fork form
    When go to the that pattern
    And click to fork button
    And the page should contains a form with "title" field

  Scenario: Forking action
    When fork the that pattern as "Forked Products"
    Then the redirected page should contains "Forked Products"
    And when click to show button
    Then the page should contains "fork-of"

  Scenario: See fork count
    When go to the profile of "tester"
    Then the page should contains "Products"
    And also the page should contains "1 fork"