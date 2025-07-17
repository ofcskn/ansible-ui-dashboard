from app.extensions import db

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.query.all()

    def get_by_id(self, id):
        return self.model.query.get(id)

    def add(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self):
        db.session.commit()

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()
