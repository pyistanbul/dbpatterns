Feature: Starring patterns
  Users can star patterns.

  Background:
    Given I am logged in as user "tester"
    And there is a pattern that named "Star Wars"
    When i am logged out
    And I am logged in as user "tester-2"

  Scenario: Star pattern
    When I star that pattern
    Then the redirected page should contains "Unstar (1)"

  Scenario: Unstar pattern
    When I star that pattern
    And again click to star button
    Then the redirected page should contains "Star (0)"

  Scenario: See star count on profile detail
    When I star that pattern
    When go to the profile of "tester"
    The page should contains "1 star"

  Scenario: See stargazers
    When I star that pattern
    When I look the stargazers of that pattern
    The page should contains "tester-2"