import psycopg2

db_params = {
    'host': 'localhost',
    'database': 'n42',
    'user': 'postgres',
    'password': '123',
    'port': 5432,
    'options': '-c search_path=dbo,sql'
}


class DbConnect:
    def __init__(self, db_params):
        self.db_params = db_params

    def __enter__(self):
        self.conn = psycopg2.connect(**self.db_params)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()


class Person:
    def __init__(self,
                 id: int | None = None,
                 name: str | None = None,
                 email: str | None = None,
                 age: int | None = None):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    def get_all(self):
        with DbConnect(db_params) as cur:
            select_query = 'SELECT id, name, email, age FROM Person;'
            cur.execute(select_query)
            persons = []
            for row in cur.fetchall():
                persons.append(Person(id=row[0], name=row[1], email=row[2], age=row[3]))
            return persons

    def get_one(id: int):
        with DbConnect(db_params) as cur:
            select_query = 'SELECT * FROM Person WHERE id = %s;'
            cur.execute(select_query, (id,))
            row = cur.fetchone()
            if row:
                return Person(id=row[1], name=row[1], email=row[2], age=row[3])
            else:
                return None

    def save(self):
        with DbConnect(db_params) as cur:
            insert_query = 'INSERT INTO Person (name, email, age) VALUES (%s, %s, %s);'
            insert_params = (self.name, self.email, self.age)
            cur.execute(insert_query, insert_params)
            print('INSERT successful')

    def __repr__(self):
        return f'Person(id={self.id}, name={self.name}, email={self.email}, age={self.age})'


person = Person(name='Javox', email='javox4ik@gmail.com', age=18)
person.save()

person_id = 2
print(Person.get_one(person_id))
