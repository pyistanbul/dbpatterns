Feature: Managing documents (patterns)

  Background: Given I am logged in as user "tester"

  Scenario: Create patterns
    When go to the create pattern page
    And I type the "title" as "Friendships"
    When I click to save button
    Then the redirected page should contains "Friendships"

  Scenario: List my patterns
    When I create a pattern that named "Customers"
    And go to the my patterns
    Then the page should contains "Customers"

  Scenario: Remove created pattern
    When I create a pattern that named "<test pattern>"
    And go to the my patterns
    Click the first delete button
    And go to the my patterns
    Then the page should not contains "<test pattern>"