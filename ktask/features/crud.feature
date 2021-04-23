Feature:
  Web Api implementes using AWS Lambda function that executes CRUD operation of TODO model
  on a DocumentDB

  Scenario:
    Add a Todo document on database...

    When The <method> event was triggered
    Then the event httpMethod should be equal to <method>