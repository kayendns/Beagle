import os

class ContentManager:
    def __init__(self, database_manager, embedder):
        self.database_manager = database_manager
        self.embedder = embedder

    def process_input_file(self, input_file):
        with open(input_file, 'r') as file:
            for line in file:
                path = line.strip()
                if os.path.exists(path):
                    self.process_path(path)
                else:
                    print(f"Path does not exist: {path}")

    def process_path(self, path):
        if os.path.isfile(path):
            self.process_file(path)
        elif os.path.isdir(path):
            self.process_directory(path)
        else:
            print(f"Invalid path: {path}")

    def process_file(self, file_path):
        # Process the file (e.g., generate embeddings)
        embedding = self.embedder.embedImage(file_path)
        # Add the file path and embedding to the database
        self.database_manager.add_element_to_database((file_path, embedding))

    def process_directory(self, directory_path):
        for root, _, files in os.walk(directory_path):
            for name in files:
                file_path = os.path.join(root, name)
                self.process_file(file_path)
