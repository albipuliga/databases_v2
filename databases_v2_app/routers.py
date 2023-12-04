class MongoDBRouter:
    """
    A database router to route certain models to MongoDB.
    """

    route_app_labels = {"databases_v2_app"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "mongodb"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "mongodb"
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return False  # Don't allow migrations for MongoDB
        return None
