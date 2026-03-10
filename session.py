import mysql.connector
import random

connection = mysql.connector.connect(host="127.0.0.1",
            port=3306,
            database="flight_game",
            user="root",
            password='y""o32',
            autocommit=True)
cursor = connection.cursor(dictionary=True)


# Check if all passengers have been used
def check_session(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM session WHERE used = 0;")
    remaining = cur.fetchone()[0]
    return remaining == 0

# If there are no unused,it'll be true

#Start game cycle

def session_start(conn):
    cur = conn.cursor()

    # Erase existing record
    cur.execute("TRUNCATE session;")

    # Insert 14 humans + 7 aliens randomly ordered
    cur.execute("""
        INSERT INTO session(passenger_id, order_index)
        SELECT id, ROW_NUMBER() OVER (ORDER BY RAND())
        FROM (
            (SELECT id FROM passenger
             WHERE true_species = TRUE
             ORDER BY RAND()
             LIMIT 14)

            UNION ALL

            (SELECT id FROM passenger
             WHERE true_species = FALSE
             ORDER BY RAND()
             LIMIT 7)
        ) AS total;
    """)

    conn.commit()


# Get the next three unused passengers
def next_three(conn):
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT so.id, passenger.*
        FROM session AS so
        JOIN passenger ON passenger.id = so.passenger_id
        WHERE so.used = 0
        ORDER BY so.order_index
        LIMIT 3;
    """)

    rows = cur.fetchall()

    # Mark the same 3 as used
    cur.execute("""
        UPDATE session
        SET used = 1
        WHERE id IN (
            SELECT id
            FROM (
                SELECT id
                FROM session
                WHERE used = 0
                ORDER BY order_index
                LIMIT 3
            ) AS sub
        );
    """)

    conn.commit()

    return rows


def main():
    conn = get_connection()

    # Start new session if everything has been used
    if check_session(conn):
        session_start(conn)

    today = next_three(conn)

    print("Today:")
    for p in today:
        print(p)

    conn.close()

def count_aliens(conn):
    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(*)
    FROM session s
    JOIN passenger p ON p.id = s.passenger_id
    WHERE s.allowed_in = 1
    AND p.true_species = FALSE;
    """)

    aliens = cur.fetchone()[0]

    return aliens

# def decisions(conn, session_id, decision):
                                            #   FUNCTION FOR DECIDING WHETHER AN ALIEN COMES IN OR NOT.WORK IN PROGRESS!
#     cur = conn.cursor()

#     cur.execute("""
#     UPDATE session
#     SET allowed_in = %s
#     WHERE id = %s
#     """, (decision, session_id))

#     conn.commit()

