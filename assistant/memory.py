import sqlite3


class Memory:
    def __init__(self, db_name="memory.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    FOREIGN KEY (conversation_id)
                        REFERENCES conversations(id)
                )
            """)

    def create_conversation(self, title="New Conversation"):
        cursor = self.conn.execute(
            "INSERT INTO conversations (title) VALUES (?)",
            (title,)
        )

        self.conn.commit()

        return cursor.lastrowid
    
    def get_conversations(self):
        cursor = self.conn.execute(
            """SELECT id, title, created_at 
            FROM conversations 
            ORDER BY created_at DESC"""
        )

        return cursor.fetchall()
    def get_conversation(self, conversation_id):
        cursor = self.conn.execute(
            """SELECT id, title, created_at 
            FROM conversations 
            WHERE id = ?""",
            (conversation_id,)
        )
        return cursor.fetchone()
    def get_conversation_title(self, conversation_id):
        cursor = self.conn.execute(
            """SELECT title 
            FROM conversations 
            WHERE id = ?""",
            (conversation_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    def get_latest_conversation(self):
        cursor = self.conn.execute(
            """SELECT id, title, created_at 
            FROM conversations 
            ORDER BY created_at DESC
            LIMIT 1"""
        )

        return cursor.fetchone()   
    
    def update_conversation_title(self, conversation_id, title):
        with self.conn:
            self.conn.execute(
                """
                UPDATE conversations 
                SET title = ? 
                WHERE id = ?
                """,
                (title, conversation_id)
            )
    
    def add_message(self, conversation_id, role, message):
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO messages
                (conversation_id, role, message)
                VALUES (?, ?, ?)
                """,
                (conversation_id, role, message)
            )

    def get_messages(self, conversation_id):
        cursor = self.conn.execute(
            """
            SELECT role, message
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (conversation_id,)
        )

        return cursor.fetchall()

    def clear_memory(self, conversation_id):
        with self.conn:
            self.conn.execute(
                "DELETE FROM messages WHERE conversation_id = ?",
                (conversation_id,)
            )
            