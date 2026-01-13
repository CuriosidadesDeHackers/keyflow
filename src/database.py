from pykeepass import PyKeePass, create_database
import os

class Database:
    def __init__(self):
        self.kp = None
        self.filepath = None
        self.password = None

    def create(self, filepath, password, keyfile=None):
        """Create a new KDBX database."""
        if os.path.exists(filepath):
            os.remove(filepath)
            
        self.kp = create_database(filepath, password=password, keyfile=keyfile)
        
        if hasattr(self.kp, 'kdf'):
            try:
                self.kp.kdf.iterations = 2
            except AttributeError:
                pass
        
        self.filepath = filepath
        self.password = password
        self.save()

    def load(self, filepath, password, keyfile=None):
        """Load an existing KDBX database."""
        try:
            self.kp = PyKeePass(filepath, password=password, keyfile=keyfile)
            self.filepath = filepath
            self.password = password
            
            if hasattr(self.kp, 'kdf'):
                try:
                    current_iterations = getattr(self.kp.kdf, 'iterations', None)
                    if current_iterations and current_iterations > 10:
                        self.kp.kdf.iterations = 2
                        self.save()
                except (AttributeError, TypeError):
                    pass
            
            return True
        except Exception as e:
            print(f"Failed to load database: {e}")
            raise e

    def save(self):
        """Save the database to disk."""
        if self.kp:
            self.kp.save()

    def add_entry(self, title, username, password, url, notes, emoji=""):
        """Add a new entry to the database."""
        if not self.kp:
            print("Error: self.kp is None")
            return None
        
        root = self.kp.root_group
        if root is None:
            print("Error: self.kp.root_group is None!")
            raise ValueError("The database file is corrupted (missing Root Group). Please 'Close Vault' and 'Create New Database' to fix this.")

        entry = self.kp.add_entry(root, title, username, password, url=url, notes=notes)
        
        # Almacenar emoji en campo personalizado si se proporciona
        if emoji:
            entry.set_custom_property("emoji", emoji)
        
        self.save()
        return entry

    def get_entries(self):
        """Get all entries from the root group (flat for now)."""
        if not self.kp:
            return []
        return self.kp.entries

    def update_entry(self, entry_uuid, title, username, password, url, notes, emoji=""):
        """Update an existing entry."""
        entry = self.kp.find_entries(uuid=entry_uuid, first=True)
        if entry:
            entry.title = title
            entry.username = username
            entry.password = password
            entry.url = url
            entry.notes = notes
            
            # Actualizar o eliminar emoji
            if emoji:
                entry.set_custom_property("emoji", emoji)
            else:
                # Si el emoji está vacío, eliminar la propiedad personalizada
                if entry.get_custom_property("emoji"):
                    entry.delete_custom_property("emoji")
            
            self.save()

    def delete_entry(self, entry_uuid):
        """Delete an entry."""
        entry = self.kp.find_entries(uuid=entry_uuid, first=True)
        if entry:
            self.kp.delete_entry(entry)
            self.save()
    
    def get_entry_emoji(self, entry):
        """Obtener el emoji de una entrada."""
        if not entry:
            return ""
        emoji = entry.get_custom_property("emoji")
        return emoji if emoji else ""
