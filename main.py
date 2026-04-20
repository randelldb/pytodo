import sqlite3

def main():
    conn = init_database()

    if conn is None:
        return False

    while True:
        should_continue = menu(conn)
        if not should_continue:
            break
        conn.close()

def menu(conn):
    clear_console()
    print("[1] View tasks")
    print("[2] Add task")
    print("[3] Delete task")
    print("[X] Exit")

    choice = input("> ").strip()

    if choice == "1":
        list_tasks(conn)
        return None
    elif choice == "2":
        add_task(conn)
        return None
    elif choice == "3":
        delete_task(conn)
        return None
    elif choice == "X":
        return False
    else:
        print("Faulty choice")
        return None


def add_task(conn):
    clear_console()
    print("Add a task")
    task_input = input()
    task = (task_input, 0)

    sql = """
        INSERT INTO tasks(name, state)
            VALUES (?,?)
    """

    cursor = conn.cursor()
    cursor.execute(sql, task)
    conn.commit()

    menu(conn)

def list_tasks(conn):
    clear_console()
    print("Current tasks:")

    sql = "SELECT * FROM tasks"

    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        print(f"[{row[0]}] - {strike(row[1])}")

    input("Press Enter to continue...")
    menu(conn)

def delete_task(conn):
    list_tasks(conn)

    print("Select a task to delete: ")
    task_id = input()

    sql = "DELETE FROM tasks WHERE id = ?"

    cursor = conn.cursor()
    cursor.execute(sql, (task_id,))
    conn.commit()

def init_database():
    sql = [
        """
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY,
                name text NOT NULL,
                state INTEGER 
            )
        """
    ]

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        for statement in sql:
            cursor.execute(statement)

        conn.commit()

        return conn
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
        return None

def clear_console():
    print("\033[H\033[J", end="")

def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result


if __name__ == '__main__':
    main()
