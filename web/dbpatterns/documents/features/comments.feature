Feature: Commenting on patterns
  Users can leave comment on patterns.

  Background:
    Given I am logged in as user "tester"
    And I create a pattern that named "Comment Model"

  Scenario: Comment pattern
    When go to the that pattern
    And I type the "body" as "Test Comment"
    When I submit the comment
    Then the comment count of that pattern should be 1

  Scenario: Display comment count
    When I leave a comment on that pattern
    And again go to the that pattern
    The page should contains "Comments (1)"

  Scenario: Display the comments of pattern
    When I leave a comment on that pattern
    And I look to the comments of that pattern
    Then the page should contains "Test Comment"