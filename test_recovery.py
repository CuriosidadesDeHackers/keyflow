from pykeepass import create_database, PyKeePass
import os

filename = "test_broken_root.kdbx"
password = "test"

if os.path.exists(filename):
    os.remove(filename)

print("Creating DB...")
kp = create_database(filename, password=password)
print(f"Initial Root: {kp.root_group}")

# Simulate deleting root
# Note: pykeepass might not allow deleting root directly or it might result in None
requests_root = kp.root_group
try:
    kp.delete_group(requests_root)
    kp.save()
    print("Deleted root group.")
except Exception as e:
    print(f"Could not delete root: {e}")

print("Reloading...")
kp = PyKeePass(filename, password=password)
print(f"Root after delete: {kp.root_group}")

try:
    if kp.root_group is None:
        print("Root is None. Attempting to add group to None...")
        # Pykeepass add_group(destination_group, group_name, ...)
        # If destination_group is None?
        try:
            kp.add_group(None, "New Root")
            print("Added group to None success.")
        except Exception as ex:
             print(f"Failed to add to None: {ex}")
             
             # Try adding to DB object or something?
             # If completely empty, maybe we can't recover easily without low level xml hacking
             # or maybe kp.add_group(kp.root_group, ...) fails obviously.
except Exception as e:
    print(e)

print(f"Entries: {kp.entries}")
    
if os.path.exists(filename):
    os.remove(filename)
