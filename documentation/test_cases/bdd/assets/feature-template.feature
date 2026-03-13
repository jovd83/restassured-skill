@API_XXX_001 @operationId @resource @smoke
Feature: Describe the API capability

  Background:
    Given the API is available
    And valid authentication is configured

  Scenario: MSS - Primary success behavior
    Given the required domain data is prepared
    When the client performs the primary API action
    Then the response status is the expected success code
    And the response body contains the expected business data

  @regression
  Scenario: EXT - Valid variant behavior
    Given the API is available
    When the client performs the variant API action
    Then the response status is the expected success code
    And the variant-specific business rules are satisfied

  @negative
  Scenario: ERR - Validation or contract-drift behavior
    Given the API is available
    When the client performs the invalid or conflicting API action
    Then the response status reflects the runtime behavior
    And the response body or mismatch notes explain the outcome
