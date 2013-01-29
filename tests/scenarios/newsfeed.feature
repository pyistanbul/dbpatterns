# Work in progress

Feature: Following users

  Background:
    Given following users exist
      | username | password |
      | edi      | 123456   |
      | budu     | 123456   |

    And "edi" following "budu"
    When I am logged in as user "edi"


  Scenario: Users can see the actions of followed profile on newsfeed
    And I go to the newsfeed
    The page should not contains "budu"
    When I am logged out
    And I am logged in as user "budu"
    And I create a pattern that named "selam"
    And I go to the that pattern
    And I type the "body" as "test comment"
    When I submit the comment
    And I am logged out
    And I am logged in as user "edi"
    And I go to the newsfeed
    The page should contains "budu"
    The page should contains "test comment"


  Scenario: The news entries of unfollowed user should be removed from newsfeed
    And I go to the newsfeed
    The page should not contains "budu"
    When I am logged out
    And I am logged in as user "budu"
    And I create a pattern that named "selam"
    And I go to the that pattern
    And I type the "body" as "test comment"
    When I submit the comment
    And I am logged out
    And I am logged in as user "edi"
    And I go to the newsfeed
    The page should contains "budu"
    The page should contains "test comment"
