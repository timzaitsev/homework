import psycopg2


def create_base():
    connection = psycopg2.connect(dbname="postgres", user="postgres", password="mypassword", host="127.0.0.1")
    cursor = connection.cursor()
    connection.autocommit = True
    sql = "CREATE DATABASE mydatabase"
    cursor.execute(sql)
    cursor.close()
    connection.close()


def create_tables():
    connection = psycopg2.connect(dbname="mydatabase", user="postgres", password="mypassword", host="127.0.0.1")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE users (id serial primary key, 
                                          name varchar(50),  
                                          email varchar(50), 
                                          password varchar(50))""")
    cursor.execute("""CREATE TABLE orders (id serial primary key, 
                                           user_id integer references users(id),
                                           cost real)""")
    connection.commit()
    cursor.close()
    connection.close()


def insert_user(name, email, password):
    connection = psycopg2.connect(dbname="mydatabase", user="postgres", password="mypassword", host="127.0.0.1")
    cursor = connection.cursor()
    sql_string = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;"
    cursor.execute(sql_string, (name, email, password))
    num = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return num


def insert_order(user_id, cost):
    connection = psycopg2.connect(dbname="mydatabase", user="postgres", password="mypassword", host="127.0.0.1")
    cursor = connection.cursor()
    sql_string = "INSERT INTO orders (user_id, cost) VALUES (%s, %s) RETURNING id;"
    cursor.execute(sql_string, (user_id, cost))
    num = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return num


def extract_users():
    connection = psycopg2.connect(dbname="mydatabase", user="postgres", password="mypassword", host="127.0.0.1")
    cursor = connection.cursor()
    get_users = """select row_to_json(t)
                     from (
                        select id, name, email
                        from users
                     ) t;
                  """
    get_orders = """select row_to_json(t)
                     from (
                        select id, user_id, cost
                        from orders
                     ) t;
                  """
    cursor.execute(get_users)
    users = cursor.fetchall()
    cursor.execute(get_orders)
    orders = cursor.fetchall()
    cursor.close()
    connection.close()
    out_data = []
    for user in users:
        total_cost = 0
        for order in orders:
            print(order)
            if user[0]['id'] == order[0]['user_id']:
                total_cost += order[0]['cost']
        out_data.append('Имя: ' + user[0]['name'] + ' Сумма: ' + str(total_cost))
    for el in out_data:
        print(el)


def extract_roles():
    connection = psycopg2.connect(dbname="mydatabase", user="postgres", password="mypassword", host="127.0.0.1")
    cursor = connection.cursor()
    get_roles = "SELECT usename, rolname FROM pg_user,pg_roles WHERE oid=usesysid;"
    cursor.execute(get_roles)
    for row in cursor.fetchall():
        print(row[0] + ',' + row[1])


if __name__ == '__main__':

    # create_base()
    # create_tables()
    # insert_user('emelya', 'emelya@ya.ru', 'qwerty')
    # insert_order(2, 1200.76)
    # extract_users()
    extract_roles()
