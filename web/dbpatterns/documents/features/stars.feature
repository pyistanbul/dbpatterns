Feature: Starring patterns
  Users can star patterns.

  Background:
    Given I am logged in as user "tester"
    And there is a pattern that named "Star Wars"
    When i am logged out
    And I am logged in as user "tester-2"
    When go to the that pattern
    And click to star button

  Scenario: Unstar that pattern
    Then the redirected page should contains "Unstar (1)"
    And again click to star button
    Then the redirected page should contains "Star (0)"

  Scenario: See star count
    When go to the profile of "tester"
    The page should contains "1 star"

  Scenario: See stargazers
    When I look the stargazers of that pattern
    The page should contains "tester-2"