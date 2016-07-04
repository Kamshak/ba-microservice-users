Feature: User service integration test
  Scenario: Register a new user
    Given Flask app is running
    When We save a user
    Then The user exists

  Scenario: Request user name
    Given Flask app is running
    And We have an user
    And We are logged in
    When We request our user
    Then The email is returned

  Scenario: Update user
    Given Flask app is running
    And We have an user
    And We are logged in
    When We update the user
    Then The user is updated

  Scenario: Login user
    Given Flask app is running
    And We have an user
    When Submit login data
    Then JWT is returned
