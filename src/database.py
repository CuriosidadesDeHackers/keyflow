from pykeepass import PyKeePass, create_database
import shutil
import os

class Database:
    def __init__(self):
        self.kp = None
        self.filepath = None
        self.password = None

    def create(self, filepath, password, keyfile=None):
        """Create a new KDBX database."""
        # Clean up if overwriting to avoid issues with existing files
        if os.path.exists(filepath):
            os.remove(filepath)
            
        self.kp = create_database(filepath, password=password, keyfile=keyfile)
        self.filepath = filepath
        self.password = password
        self.save()

    def load(self, filepath, password, keyfile=None):
        """Load an existing KDBX database."""
        try:
            self.kp = PyKeePass(filepath, password=password, keyfile=keyfile)
            self.filepath = filepath
            self.password = password
            return True
        except Exception as e:
            print(f"Failed to load database: {e}")
            raise e

    def save(self):
        """Save the database to disk."""
        if self.kp:
            self.kp.save()

    def add_entry(self, title, username, password, url, notes, group=None):
        """Add a new entry to the database."""
        if not self.kp:
            return None
        
        if group is None:
            group = self.kp.root_group

        entry = self.kp.add_entry(group, title, username, password, url=url, notes=notes)
        self.save()
        return entry

    def get_entries(self):
        """Get all entries from the root group (flat for now)."""
        if not self.kp:
            return []
        # Recursive fetch could be added here, but flat list of all entries for now
        return self.kp.entries

    def update_entry(self, entry_uuid, title, username, password, url, notes):
        """Update an existing entry."""
        entry = self.kp.find_entries(uuid=entry_uuid, first=True)
        if entry:
            entry.title = title
            entry.username = username
            entry.password = password
            entry.url = url
            entry.notes = notes
            self.save()

    def delete_entry(self, entry_uuid):
        """Delete an entry."""
        entry = self.kp.find_entries(uuid=entry_uuid, first=True)
        if entry:
            self.kp.delete_entry(entry)
            self.save()
