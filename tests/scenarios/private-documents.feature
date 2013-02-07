Feature: Private Documents
  In order to create documents which can be seen by just me,
  As an authenticated user,
  I want to create a private document.

  Background:
    Given following users exist
      | username | password |
      | edi      | 123456   |
      | budu     | 123456   |

    When I am logged in as user "edi"

  Scenario: Create private patterns
    When go to the create pattern page
    And I type the "title" as "Friendships"
    And I choose the "is_public" option as "False"
    When I click to save button
    Then the redirected page should contains "Make Public"

  Scenario: The others can not see the private documents
    When go to the create pattern page
    And I type the "title" as "Hey, it's just me"
    And I choose the "is_public" option as "False"
    When I click to save button
    And I am logged out
    And I am logged in as user "budu"
    And I go to the created pattern
    Then the page should return with 404 status code.

  Scenario: The creator of a private pattern can make it public
    When go to the create pattern page
    And I type the "title" as "Hey, I make it public after the organizing"
    And I choose the "is_public" option as "False"
    When I click to save button
    And click to the make public button
    And I am logged out
    And I am logged in as user "budu"
    And I go to the created pattern
    Then the page should contains "Hey, I make it public after the organizing"

  Scenario: Private patterns can't be visible on the newsfeed.
    When go to the create pattern page
    And I type the "title" as "Secret work"
    And I choose the "is_public" option as "False"
    When I click to save button
    And I go to the newsfeed
    The page should not contains "Secret work"
