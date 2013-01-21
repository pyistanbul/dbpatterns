Feature: Following users

  Background:
    Given following users exist
      | username | password |
      | edi      | 123456   |
      | budu     | 123456   |

    When I am logged in as user "edi"

  Scenario: users can follow the others
    When I go to the profile of "budu"
    And I click to follow button
    And I go to the profile of "budu" again
    Then the page should contains "edi following budu"

  Scenario: see followed profiles on the profile of follower
    When I go to the profile of "budu"
    And I click to follow button
    And I go to my profile
    Then the page should contains "edi following budu"

  Scenario: users can't follow himself
    When go to my profile
    The page should not contains "Follow"
    The page should not contains "Unfollow"

  Scenario: users can't follow already followed users
    When I go to the profile of "budu"
    And I click to follow button
    And I go to the profile of "budu" again
    And the page should not contains "Follow"
    And the page should contains "Unfollow"

  Scenario: users can't follow already followed profiles
    When I go to the profile of "budu"
    And I click to follow button
    When go to the profile of "budu" again
    The page should not contains "Follow"
    The page should contains "Unfollow"

  Scenario: user can unfollow followed profiles
    When I go to the profile of "budu"
    And I click to follow button
    And go to the profile of "budu" again
    And when click to unfollow button
    And I go to the profile of "budu" again
    Then the page should contains "Follow"
    And the page should not contains "Unfollow"