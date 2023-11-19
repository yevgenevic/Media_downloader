import psycopg2

db_config = {
    'dbname': 'download',
    'user': 'postgres',
    'password': '1',
    'host': 'localhost',
    'port': 5432
}

connection = psycopg2.connect(**db_config)
cursor = connection.cursor()


def create_tabel():
    user_table = '''
        CREATE TABLE IF NOT EXISTS users (
            id serial primary key,
            name varchar(100) unique,
            user_id varchar(20),
            block bool DEFAULT TRUE,
            created_at timestamp default current_timestamp
        )
    '''

    admin_table = '''
            CREATE TABLE IF NOT EXISTS admin_tabel(
                id serial primary key,
                name varchar(100) unique,
                user_id varchar(20),
                created_at timestamp default current_timestamp
            )
        '''
    cursor.execute(user_table)
    cursor.execute(admin_table)
    connection.commit()


def create_user(name: str, user_id: int):
    query = "INSERT INTO users (name, user_id) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING"
    cursor.execute(query, (name, user_id))
    connection.commit()


def check_admin(admin_id: str):
    query = "SELECT * FROM admin_tabel WHERE user_id = %s"
    cursor.execute(query, (admin_id,))
    data = cursor.fetchone()
    if data:
        que = "SELECT * FROM users"


create_tabel()
