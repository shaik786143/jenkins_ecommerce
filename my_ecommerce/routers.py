class AnalyticsRouter:
    """
    A router to control all database operations on models in the
    analytics application.
    """

    route_app_labels = {"reporting"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read reporting models go to analytics_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "analytics_db"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write reporting models go to analytics_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "analytics_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the reporting app is involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the reporting app only appears in the 'analytics_db'
        database.
        """
        if app_label in self.route_app_labels:
            return db == "analytics_db"
        return None 