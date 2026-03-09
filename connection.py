import mariadb

def get_connection():
    return mariadb.connect(
        user="root",
        password='y""o32',
        host="127.0.0.1",
        port=3306,
        database="flight_game"
    )

