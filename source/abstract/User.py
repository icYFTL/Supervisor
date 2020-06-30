class User(object):
    def __init__(self, id: int, imprisonment_counter=0, total_time=0, kicked_by=None):
        self.id = id
        self.imprisonment_counter = imprisonment_counter
        self.total_time = total_time
        self.kicked_by = kicked_by or None

    def __repr__(self):
        return f'<User ID: {self.id}>'

    def __iter__(self):
        yield 'id', self.id
        yield 'imprisonment_counter', self.imprisonment_counter
        yield 'total_time', self.total_time
        yield 'kicked_by', self.kicked_by
