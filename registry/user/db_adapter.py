
class DBAdapter(object):

    def __init__(self, db, UserClass):
        self.db = db
        self.UserClass = UserClass


class SQLAlchemyAdapter(DBAdapter):

    def __init__(self, db, UserClass):
        super(SQLAlchemyAdapter, self).__init__(db, UserClass)

    def find_all_objects(self, ObjectClass, **kwargs):
        query = ObjectClass.query
        for filed_name, filed_value in kwargs.items():
            filed = getattr(ObjectClass, filed_name, None)
            if filed is None:
                raise KeyError('SQLAlchemyAdapter.find_all_objects(): class %s has no filed %s' % (ObjectClass, filed))
            query = query.filter(filed.in_((filed_value,)))
        return query.all()

    def find_first_object(self, ObjectClass, **kwargs):
        query = ObjectClass.query
        for filed_name, filed_value in kwargs.items():
            filed = getattr(ObjectClass, filed_name, None)
            if filed is None:
                raise KeyError('SQLAlchemyAdapter.find_first_object(): class %s has no filed %s' % (ObjectClass, filed))
            query = query.filter(filed==filed_value)
        return query.first()

    def get_object(self, ObjectClass, id):
        return ObjectClass.query.get(id)

    def add_object(self, ObjectClass, **kwargs):
        object = ObjectClass(**kwargs)
        self.db.session.add(object)
        return object

    def update_object(self, object, **kwargs):
        for key, value in kwargs.items():
            if hasattr(object, key):
                setattr(object, key, value)
            else:
                raise KeyError('Object %s has no filed %s' % type(object), key)

    def delete_object(self, object):
        self.db.session.delete(object)

    def commit(self):
        self.db.session.commit()

