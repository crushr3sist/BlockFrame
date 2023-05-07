class BlockFrameDatabaseSetters:
    def __init__(self, *args, **kwargs):
        self.db = kwargs.get("database_obj")
        self.model = kwargs.get("class_model")

    def get_ammount(self):
        return len(self.db.query.all())
