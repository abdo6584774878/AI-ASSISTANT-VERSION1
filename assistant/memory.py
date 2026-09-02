import sqlite3


class Memory:
    def __init__(self, user_id=0, db_name="memory.db"):
        #backward compatibility: 
        # old code/tests can still use Memory(":memory:")
        if isinstance(user_id, str) and user_id == ":memory:":
            db_name = ":memory:"
            user_id = 0
        self.user_id = user_id
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # ---------------------------------------------------------
            # CONVERSATIONS
            # ---------------------------------------------------------
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL DEFAULT 0,
                    title TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # ---------------------------------------------------------
            # MESSAGES
            # ---------------------------------------------------------
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

            # ---------------------------------------------------------
            # MEMORIES
            # ---------------------------------------------------------
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL DEFAULT 0,
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # ---------------------------------------------------------
            # MIGRATION FOR EXISTING DATABASES
            # ---------------------------------------------------------

            conversation_columns = self.conn.execute(
                "PRAGMA table_info(conversations)"
            ).fetchall()

            conversation_column_names = [column[1] for column in conversation_columns]

            if "user_id" not in conversation_column_names:
                self.conn.execute("""
                    ALTER TABLE conversations
                    ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0
                """)

            memory_columns = self.conn.execute("PRAGMA table_info(memories)").fetchall()

            memory_column_names = [column[1] for column in memory_columns]

            if "user_id" not in memory_column_names:
                self.conn.execute("""
                    ALTER TABLE memories
                    ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0
                """)

    # ============================================================
    # CONVERSATIONS
    # ============================================================

    def create_conversation(self, title="New Conversation"):
        cursor = self.conn.execute(
            """
            INSERT INTO conversations (user_id, title)
            VALUES (?, ?)
            """,
            (self.user_id, title),
        )

        self.conn.commit()

        return cursor.lastrowid

    def get_conversations(self):
        cursor = self.conn.execute(
            """
            SELECT id, title, created_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (self.user_id,),
        )

        return cursor.fetchall()

    def get_conversation(self, conversation_id):
        cursor = self.conn.execute(
            """
            SELECT id, title, created_at
            FROM conversations
            WHERE id = ?
            AND user_id = ?
            """,
            (conversation_id, self.user_id),
        )

        return cursor.fetchone()

    def get_conversation_title(self, conversation_id):
        cursor = self.conn.execute(
            """
            SELECT title
            FROM conversations
            WHERE id = ?
            AND user_id = ?
            """,
            (conversation_id, self.user_id),
        )

        result = cursor.fetchone()

        return result[0] if result else None

    def get_latest_conversation(self):
        cursor = self.conn.execute(
            """
            SELECT id, title, created_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT 1
            """,
            (self.user_id,),
        )

        return cursor.fetchone()

    def update_conversation_title(self, conversation_id, title):
        with self.conn:
            self.conn.execute(
                """
                UPDATE conversations
                SET title = ?
                WHERE id = ?
                AND user_id = ?
                """,
                (title, conversation_id, self.user_id),
            )

    def delete_conversation(self, conversation_id):
        with self.conn:
            self.conn.execute(
                """
                DELETE FROM messages
                WHERE conversation_id = ?
                """,
                (conversation_id,),
            )

            cursor = self.conn.execute(
                """
                DELETE FROM conversations
                WHERE id = ?
                AND user_id = ?
                """,
                (conversation_id, self.user_id),
            )

        return cursor.rowcount > 0

    # ============================================================
    # MESSAGES
    # ============================================================

    def add_message(self, conversation_id, role, message):
        # Make sure the conversation belongs to this user.
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            raise ValueError("Conversation not found.")

        with self.conn:
            self.conn.execute(
                """
                INSERT INTO messages
                (conversation_id, role, message)
                VALUES (?, ?, ?)
                """,
                (conversation_id, role, message),
            )

    def get_messages(self, conversation_id):
        # Make sure the conversation belongs to this user.
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            return []

        cursor = self.conn.execute(
            """
            SELECT role, message
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (conversation_id,),
        )

        return cursor.fetchall()

    def clear_memory(self, conversation_id):
        # Make sure the conversation belongs to this user.
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            return False

        with self.conn:
            self.conn.execute(
                """
                DELETE FROM messages
                WHERE conversation_id = ?
                """,
                (conversation_id,),
            )

        return True

    # ============================================================
    # MEMORIES
    # ============================================================

    def create_memory(self, category, key, value):
        existing = self.conn.execute(
            """
            SELECT id
            FROM memories
            WHERE user_id = ?
            AND category = ?
            AND key = ?
            AND value = ?
            """,
            (
                self.user_id,
                category,
                key,
                value,
            ),
        ).fetchone()

        if existing:
            return existing[0]

        cursor = self.conn.execute(
            """
            INSERT INTO memories
            (user_id, category, key, value)
            VALUES (?, ?, ?, ?)
            """,
            (
                self.user_id,
                category,
                key,
                value,
            ),
        )

        self.conn.commit()

        return cursor.lastrowid

    def get_memory(self, memory_id):
        cursor = self.conn.execute(
            """
            SELECT id, category, key, value, created_at, updated_at
            FROM memories
            WHERE id = ?
            AND user_id = ?
            """,
            (memory_id, self.user_id),
        )

        return cursor.fetchone()

    def get_memories(self):
        cursor = self.conn.execute(
            """
            SELECT id, category, key, value, created_at, updated_at
            FROM memories
            WHERE user_id = ?
            ORDER BY id
            """,
            (self.user_id,),
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
                AND user_id = ?
                """,
                (
                    category,
                    key,
                    value,
                    memory_id,
                    self.user_id,
                ),
            )

        return cursor.rowcount > 0

    def delete_memory(self, memory_id):
        with self.conn:
            cursor = self.conn.execute(
                """
                DELETE FROM memories
                WHERE id = ?
                AND user_id = ?
                """,
                (memory_id, self.user_id),
            )

        return cursor.rowcount > 0

    def search_memories(self, query):
        words = query.lower().split()

        if not words:
            return []

        conditions = []
        parameters = [self.user_id]

        for word in words:
            conditions.append("(LOWER(key) LIKE ? OR LOWER(value) LIKE ?)")

            parameters.extend(
                [
                    f"%{word}%",
                    f"%{word}%",
                ]
            )

        cursor = self.conn.execute(
            f"""
            SELECT id, category, key, value, created_at, updated_at
            FROM memories
            WHERE user_id = ?
            AND ({" OR ".join(conditions)})
            ORDER BY id
            """,
            parameters,
        )

        return cursor.fetchall()
