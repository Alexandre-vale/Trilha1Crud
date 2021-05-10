# TODO Api

## Endpoints

1. CREATE:
    - Method: POST
    - PATH:
      - /todo
    - request body:
    ```json
        {
          "name": "Example",
          "body": "testetetetetete",
          "owner": "teste@teste.com",
          "access": {  
            "readers": [],
            "contributors": []
          },
          "deadline": "2021-06-15",
          "notification": "2021-05-26",
          "status": false
        }
     ```
    * response:
     ```json
        { "todos":
            [
                {
                  "name": "Example",
                  "body": "testetetetetete",
                  "owner": "teste@teste.com",
                  "access": {  
                    "readers": [],
                    "contributors": []
                  },
                  "created_at": "2021-04-16",
                  "lastupdate": {"date": "2021-04-16"},
                  "deadline": "2021-06-15",
                  "notification": "2021-05-26",
                  "status": false
                }
            ] 
        }
     ```
    
---
2. READ
   * Method: GET
   * PATH: 
     - /todo,
     - /todo?id=<todo_id>
   * request body: empty
   * response:
    ```json
        { "todos":
            [
                {
                  "name": "Example",
                  "body": "testetetetetete",
                  "owner": "teste@teste.com",
                  "access": {  
                    "readers": [],
                    "contributors": []
                  },
                  "created_at": "2021-04-16",
                  "lastupdate": "2021-04-16",
                  "deadline": "2021-06-15",
                  "notification": "2021-05-26",
                  "status": false
                }
            ] 
        }
    ```

---

3. Update:
    * Method: PUT
   * PATH: 
     - /todo?id=<todo_id>
   * request body
     ```json
        {
            "name": "testezin"
        }
     ```
   * response:
    ```json
        { "todos":
            [
                {
                  "name": "testezin",
                  "body": "testetetetetete",
                  "owner": "teste@teste.com",
                  "access": {  
                    "readers": [],
                    "contributors": []
                  },
                  "created_at": "2021-04-16",
                  "lastupdate": "2021-04-16",
                  "deadline": "2021-06-15",
                  "notification": "2021-05-26",
                  "status": false
                }
            ] 
        }
    ```
    
---

4. Delete
    * Method: DELETE
   * PATH: 
     - /todo?id=<todo_id>
   * request body: empty
   * response:
    ```json
        {
          "message": "successfully deleted"
        }  
    ```
