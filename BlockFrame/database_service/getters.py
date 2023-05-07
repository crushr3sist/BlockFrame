class BlockFrameDatabaseGetters:
    def __init__(self, *args, **kwargs):
        self.db = kwargs.get("database_obj")
        self.model = kwargs.get("class_model")

    def get_all(self):
        with self.db as session:
            result = session.query(self.model).all()
        return result

    def get_amount(self):
        return len(self.db.query.all())
