import sqlite3
import os
import torch
import numpy as np

class DatabaseManager:
    def __init__(self, db_path='embeddings.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect('database.db', check_same_thread=False)  # Persistent connection
        self._initialize_db()
        self.cleanup_database()

    def _initialize_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS embeddings 
                          (file_path TEXT PRIMARY KEY, embedding BLOB)''')
        self.conn.commit()

    def cleanup_database(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT file_path FROM embeddings')
        rows = cursor.fetchall()
        for row in rows:
            file_path = row[0]
            if not os.path.exists(file_path):
                self.delete_element_from_database(file_path)

    # Convert Tensor into binary, so it can be stored as a BLOB in SQLite
    def _convert_tensor_to_bytes(self, tensor: torch.Tensor) -> bytes:
        # Ensure the tensor is on the CPU
        tensor = tensor.cpu()
        return tensor.numpy().tobytes()


    def _convert_blob_to_tensor(self, blob) -> torch.Tensor:
        data = np.frombuffer(blob, dtype=np.float16)
        tensor = torch.tensor(data)
        return tensor.to("cuda" if torch.cuda.is_available() else "cpu")

    def add_element_to_database(self, element: tuple):
        file_path, tensor = element
        cursor = self.conn.cursor()
        embedding_bytes = self._convert_tensor_to_bytes(tensor)
        # Use INSERT OR IGNORE to add the element only if it doesn't already exist
        cursor.execute('INSERT OR IGNORE INTO embeddings (file_path, embedding) VALUES (?, ?)',
                    (file_path, embedding_bytes))
        self.conn.commit()


    def get_entry_by_file_path(self, file_path):
        cursor = self.conn.cursor()
        cursor.execute('SELECT embedding FROM embeddings WHERE file_path = ?', (file_path,))
        return cursor.fetchone()

    def fetch_all_embeddings(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT file_path, embedding FROM embeddings')
        rows = cursor.fetchall()
        return [(file_path, self._convert_blob_to_tensor(embedding_blob)) for file_path, embedding_blob in rows]

    def delete_element_from_database(self, elementName):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM embeddings WHERE file_path = ?', (elementName,))
        self.conn.commit()

    def close(self):
        self.conn.close()
