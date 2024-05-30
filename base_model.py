import uuid
from datetime import datetime
import sqlite3

DATABASE = 'my_database.db'

class BaseModel:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now().isoformat())
        self.updated_at = kwargs.get('updated_at', datetime.now().isoformat())
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        self.updated_at = datetime.now().isoformat()
        columns = ', '.join(self.__dict__.keys())
        placeholders = ', '.join(['?' for _ in self.__dict__.keys()])
        values = tuple(self.__dict__.values())

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.__class__.__name__} (
                    id TEXT PRIMARY KEY,
                    created_at TEXT,
                    updated_at TEXT,
                    {self.additional_columns()}
                )
            """)
            cursor.execute(f"""
                INSERT OR REPLACE INTO {self.__class__.__name__} ({columns})
                VALUES ({placeholders})
            """, values)
            conn.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def delete(self):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {self.__class__.__name__} WHERE id=?", (self.id,))
            conn.commit()

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def get(cls, record_id):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {cls.__name__} WHERE id=?", (record_id,))
            row = cursor.fetchone()
            if row:
                keys = [column[0] for column in cursor.description]
                return cls(**dict(zip(keys, row)))
            return None

    @classmethod
    def all(cls):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {cls.__name__}")
            rows = cursor.fetchall()
            keys = [column[0] for column in cursor.description]
            return [cls(**dict(zip(keys, row))) for row in rows]

    @classmethod
    def create_table(cls):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {cls.__name__} (
                    id TEXT PRIMARY KEY,
                    created_at TEXT,
                    updated_at TEXT,
                    {cls.additional_columns()}
                )
            """)
            conn.commit()

    @classmethod
    def additional_columns(cls):
        return "name TEXT, my_number INTEGER"  # Override this method in subclasses to add columns

    @staticmethod
    def column_exists(table, column):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [info[1] for info in cursor.fetchall()]
            return column in columns

    @staticmethod
    def add_foreign_key(table, column, ref_table, ref_column):
        if not BaseModel.column_exists(table, column):
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA foreign_keys = ON")
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")
                cursor.execute(f"""
                    CREATE TRIGGER IF NOT EXISTS fk_check_{table}_{column} BEFORE INSERT ON {table}
                    FOR EACH ROW BEGIN
                        SELECT RAISE(ABORT, 'Foreign key violation')
                        WHERE (SELECT id FROM {ref_table} WHERE id = NEW.{column}) IS NULL;
                    END;
                """)
                conn.commit()