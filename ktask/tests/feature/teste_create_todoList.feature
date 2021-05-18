Feature: Create a todoList
    Scenario: Create a todoList using valid data
        Given A user whit valid acess tokens
        And the user wants create a todolist with name as "Object Oriented work"
        And the description of the todolist is "Intenface studies"
        And owner of the todolist is "fulano@gmail.com"
        And access as a todolist contribution is "fuba2@gmail.com"
        And reader access as a todolist  is "bolinho@gmail.com"
        And the todolist deadline date is "2021-05-02"
    When user submits the todolist data in "http://localhost:3000/todolist"
        Then you should receive a "200" status code
        And name "Object Oriented work" should be in response body
        And description "Intenface studies" should be in response body
        And owner "fulano@gmail.com" should be in response body
        And acess contributor "fuba2@gmail.com" should be in response body
        And access reader "bolinho@gmail.com" should be in response body
        And deadline date "2021-05-02" should be in response body