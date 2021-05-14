# TODO Api

API implementada para o teste técnico proposto para consolidar o conhecimento
adquirido na trilha dev dos estagiários da Kumulus.

A Api consiste na manipulação de duas entiades em si: TodoList
e ToDo, onde cada Todo pertence a uma TodoList. Os endpoints implementados permitem 
as operações básicas de CRUD e filtragem de dados, bem como o pre-signed no s3 da AWS

Como tecnologia utilizamos:
- AWS lambda para processar eventos
- DocumentDB como banco de dados
- AWS EKS para o deploy da API

## Instalação

Pré-Requisitos:
- [AWS cli](https://aws.amazon.com/cli/)
- [AWS SAM cki](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Docker](https://docs.docker.com/engine/install/)
- git

1. clone o repositório na sua máquina:
   ```shell
   $ git clone git@github.com:Alexandre-vale/Trilha1Crud.git
   ```

2. crie os arquivos .env:
   ````shell
   $ cd ktask
   $ cp ../contrib/env-crud ./crudapi/.env
   $ cp ../contrib/env-upload ./upload/.env
   ````

3. Faça o build para gerar a imagem docker das funções lambda:
   ```shell
   $ sam build
   ```

## How to run
   ````shell
   $ sam local start-api
   ````

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

---

5. Filter by owner
   * Method: GET
   * PATH:
     Get ToDos by owner:
      - /get_by_owner?owner=<owner_email>&list=False 
        
     Get TodoLists by owner:
      - /get_by_owner?owner=<owner_email>&list=True
      
   * request body: empty
   * response: Uma lista de todos ou todolists, dependendo do parametro list
   
---

6. Filter by status
   * Method: GET
   * PATH:
     Get ToDos by status:
      - /get_by_status?status=<status>&list=False 
        
     Get TodoLists by status:
      - /get_by_status?status=<status>&list=True
      
   * request body: empty
   * response: Uma lista de todos ou todolists, dependendo do parametro list
   
---

7. Filter by access
   * Method: GET
   * PATH:
      - /get_by_status?contributor=<contributor_email>
      
   * request body: empty
   * response: Uma lista todolists
   
---

8. Get Pre-Signed URL
   * Method: GET
   * PATH:
      - /get_upload_url?key=<nome_do_arquivo>
   * request body: empty
   * response:
      ````json
      {
        "url": "<pre_signed_url>"
      }
      ````