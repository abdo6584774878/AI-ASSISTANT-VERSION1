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
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            ORDER BY created_at DESC, id DESC
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
    
    def delete_conversation(self, conversation_id):
        with self.conn:
            self.conn.execute(
                "DELETE FROM messages WHERE conversation_id = ?",
                (conversation_id,)
            )
            cursor = self.conn.execute(
                "DELETE FROM conversations WHERE id = ?",
                (conversation_id,)
            )
        return cursor.rowcount > 0 # Return True if any rows were deleted
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
    
    def create_memory(self, category, key, value):
        existing = self.conn.execute(
            """
            SELECT id
            FROM memories
            WHERE category = ?
            AND key = ?
            AND value = ?
            """,
            (category, key, value)
        ).fetchone()

        if existing:
            return existing[0]
        cursor = self.conn.execute(
            """
            INSERT INTO memories
            (category, key, value)
            VALUES (?, ?, ?)
            """,
            (category, key, value)
        )
        
        self.conn.commit()
        
        return cursor.lastrowid
    def get_memory(self, memory_id):
        cursor = self.conn.execute(
        """
        SELECT id, category, key, value, created_at, updated_at
        FROM memories
        WHERE id = ?
        """,
        (memory_id,)
        )
        
        return cursor.fetchone()
    def get_memories(self):
        cursor = self.conn.execute(
        """
        SELECT id, category, key, value, created_at, updated_at
        FROM memories
        ORDER BY id
        """
        )
        return cursor.fetchall()
    def update_memory(self, memory_id, category, key, value):
        with self.conn:
            cursor = self.conn.execute(
                """
                UPDATE memories
                SET category = ?,
                    key = ?,
                    value = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (category, key, value, memory_id)
            )
        return cursor.rowcount > 0
    def delete_memory(self, memory_id):
        with self.conn:
            cursor = self.conn.execute(
                """
                DELETE FROM memories
                WHERE id = ?
                """,
                 (memory_id,)
        )
        return cursor.rowcount > 0
    def search_memories(self, query):
        words = query.lower().split()
        
        if not words:
            return[]
        conditions = []
        parameters = []
        
        for word in words:
            conditions.append(
                "(LOWER(key) LIKE ? OR LOWER(value) LIKE ?)"
            )
            parameters.extend([
                f"%{word}%",
                f"%{word}%"
            ])
        cursor = self.conn.execute(
        f"""
        SELECT id, category, key, value, created_at, updated_at
        FROM memories
        WHERE {" OR ".join(conditions)}
        ORDER BY id
        """,
        parameters
        )
        return cursor.fetchall()