import sqlite3

def init_db():
    conn = sqlite3.connect("todo_manager.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        due_date TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
    """)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def signup():
    print("\n-- Sign Up --")
    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()

    if not username or not password:
        print("Invalid input.")
        return None

    conn = sqlite3.connect('todo_manager.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Username already exists. Try another one.")
        conn.close()
        return None

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()
    conn.close()
    print("Account created successfully. You can now log in.")
    return None

def login():
    print("\n-- Login --")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    conn = sqlite3.connect('todo_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"Welcome, {username}!")
        return {"id": user[0], "username": user[1]}
    else:
        print("Invalid login.")
        return None

def add_todo():
    print("\n-- Add To-Do --")
    title = input("To-Do: ").strip()
    if not title:
        print("To-Do cannot be empty.")
        return

    due_date = input("Due date (YYYY-MM-DD): ").strip()

    conn = sqlite3.connect("todo_manager.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title, due_date) VALUES (?, ?)", (title, due_date))
    conn.commit()
    conn.close()

    print("To-Do saved!")

def list_todos():
    print("\n-- To-Do List --")
    conn = sqlite3.connect("todo_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, due_date, completed FROM todos")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No to-dos found.")
        return

    print("ID | Task           | Due Date   | Status")
    print("---------------------------------------------")

    for row in rows:
        status = "✅" if row[3] == 1 else "❌"
        print(f"{row[0]:<2} | {row[1]:<14} | {row[2]:<10} | {status}")


def complete_todo():
    print("\n-- Complete To-Do --")
    list_todos()
    conn = sqlite3.connect("todo_manager.db")
    cursor = conn.cursor()

    todo_id = input("Enter ID to complete: ").strip()

    cursor.execute("SELECT completed FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()

    if not row:
        print("No task found with that ID.")
    elif row[0] == 1:
        print("⚠️ Task is already completed.")
    else:
        cursor.execute("UPDATE todos SET completed = 1 WHERE id = ?", (todo_id,))
        conn.commit()
        print("✅ To-Do marked as complete.")
        list_todos()
        conn.close()

def edit_todo():
    print("\n-- Edit To-Do --")
    list_todos()

    todo_id = input("Enter the ID of the to-do to edit: ").strip()
    if not todo_id.isdigit():
        print("Invalid ID.")
        return

    new_title = input("New title (leave blank to keep current): ").strip()
    new_due_date = input("New due date (YYYY-MM-DD, leave blank to keep current): ").strip()

    conn = sqlite3.connect("todo_manager.db")
    cursor = conn.cursor()

    # Fetch existing row
    cursor.execute("SELECT title, due_date FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if not row:
        print("No task found with that ID.")
        conn.close()
        return

    # Keep old values if new ones are blank
    title = new_title if new_title else row[0]
    due_date = new_due_date if new_due_date else row[1]

    cursor.execute("UPDATE todos SET title = ?, due_date = ? WHERE id = ?", (title, due_date, todo_id))
    conn.commit()
    conn.close()

    print("✏️ To-Do updated successfully.")

def delete_todo():
    print("\n-- Delete To-Do --")
    # Show all todos first
    list_todos()

    todo_id = input("Enter the ID of the to-do to delete: ").strip()
    if not todo_id.isdigit():
        print("Invalid ID.")
        return

    conn = sqlite3.connect("todo_manager.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()

    if not row:
        print("No task found with that ID.")
    else:
        confirm = input(f"Are you sure you want to delete task '{row[1]}'? (y/n): ").strip().lower()
        if confirm == "y":
            cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            conn.commit()
            print("🗑️ To-Do deleted successfully.")
        else:
            print("❌ Delete cancelled.")

    conn.close()


def main():
    init_db()
    print("=== To-Do Manager App ===")

    user = None
    while not user:
        print("\n1. Login")
        print("2. Sign up")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = login()
        elif choice == "2":
            signup()
        else:
            print("Invalid choice. Try again.")

    # Main menu loop
    while True:
        print("\nMenu:")
        print("1. Add To-Do")
        print("2. List To-Dos")
        print("3. Complete To-Do")
        print("4. Edit To-Do")
        print("5. Delete To-Do")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_todo()
        elif choice == "2":
            list_todos()
        elif choice == "3":
            complete_todo()
        elif choice == "4":
            edit_todo()
        elif choice == "5":
            delete_todo()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()


