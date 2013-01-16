Feature: Create and manage documents

  Scenario: Create a pattern that called Friendships
    Given I am logged in as user "tester"
    When go to the create pattern page
    And I type the title as "Friendships"
    When I click to save button
    Then the page should redirect to edit page
    And the redirected page should contains "Friendships"

  Scenario: List my patterns
    Given I am logged in as user "tester"
    And create a pattern that named "Customers"
    When go to the my patterns
    Then the page should contains "Customers"