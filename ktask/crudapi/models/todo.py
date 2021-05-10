from mongoengine import Document, StringField, DateField, DictField, BooleanField


class ToDoList(Document):
    """
    TodoList model  abstraction
    """

    name = StringField(max_length=30)
    description = StringField(max_length=255)
    owner = StringField()
    todos = DictField()
    access = DictField()
    created_at = DateField()
    last_update = DictField()
    deadline = DateField()
    notification = DateField()
    status = StringField()

    def serialize(self) -> dict:
        return {
            "id": str(self.pk),
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "todos": self.todos,
            "access": self.access,
            "created_at": str(self.created_at),
            "lastupdate": {
                "user": self.last_update["user"],
                "date": str(self.last_update["date"]),
                "todo": self.last_update["todo"]
            },
            "deadline": str(self.deadline),
            "notification": str(self.notification),
            "status": self.status,
        }


class ToDo(Document):
    """
    Todo model abstraction
    """

    name = StringField(max_length=30)
    body = StringField()
    owner = StringField()
    todolist = StringField()
    assigment = StringField()
    created_at = DateField()
    last_update = DictField()
    deadline = DateField()
    notification = DateField()
    status = StringField()
    attachments = DictField()

    def serialize(self) -> dict:
        return {
            "id": str(self.pk),
            "name": self.name,
            "body": self.body,
            "owner": self.owner,
            "todolist": self.todolist,
            "assigment": self.assigment,
            "created_at": str(self.created_at),
            "lastupdate":{
                "user": self.last_update["user"],
                "date": str(self.last_update["date"]),
            },
            "deadline": str(self.deadline),
            "notification": str(self.notification),
            "status": self.status,
            "attachments": self.attachments,
        }
