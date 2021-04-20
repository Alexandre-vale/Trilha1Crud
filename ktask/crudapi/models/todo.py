from mongoengine import Document, StringField, DateField, DictField, BooleanField


class ToDo(Document):
    """
    Todo model abstraction
    """

    name = StringField(max_length=30)
    body = StringField()
    owner = StringField()
    contribuitors = DictField()
    created_at = DateField()
    last_update = DateField()
    deadline = DateField()
    notification = DateField()
    status = BooleanField()


    def serialize(self) -> dict:
        return {
            "id": str(self.pk),
            "name": self.name,
            "body": self.body,
            "owner": self.owner,
            "contribuitors": self.contribuitors,
            "created_at": str(self.created_at),
            "lastupdate": str(self.last_update),
            "deadline": str(self.deadline),
            "notification": str(self.notification),
            "status": self.status
        }
