Feature: Managing documents (patterns)

  Scenario: Create patterns
    Given I am logged in as user "tester"
    When go to the create pattern page
    And I type the title as "Friendships"
    When I click to save button
    Then the redirected page should contains "Friendships"

  Scenario: List my patterns
    Given I am logged in as user "tester"
    And I create a pattern that named "Customers"
    When go to the my patterns
    Then the page should contains "Customers"

  Scenario: Remove created pattern
    Given I am logged in as user "tester"
    And I create a pattern that named "<test pattern>"
    When go to the my patterns
    Click the first delete button
    And go to the my patterns
    Then the page should not contains "<test pattern>"