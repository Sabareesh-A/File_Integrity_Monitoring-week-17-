import os
import hashlib
import time
import json

folder_path = "/Users/sabareeshanil/Desktop/fim/periodic_fim/file_dir"

def process_file(file_path, new_hashes):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    file_name = os.path.basename(file_path)
    current_time = time.ctime()

    new_hashes[file_name] = {
        "hash": file_hash,
        "timestamp": current_time
    }

if not os.path.exists("baseline.json"):
    initial_hashes = {}
    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if os.path.isfile(full_path):
            process_file(full_path, initial_hashes)

    with open("baseline.json", "w") as f:
        json.dump(initial_hashes, f, indent=4)

while True:
    new_hashes = {}
    changes = {
        "modified": [],
        "added": [],
        "deleted": []
    }

    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if os.path.isfile(full_path):
            process_file(full_path, new_hashes)

    with open("baseline.json", "r") as f:
        existing_hashes = json.load(f)

    for file in existing_hashes:
        if file in new_hashes:
            if existing_hashes[file]["hash"] != new_hashes[file]["hash"]:
                changes["modified"].append(file + " modified at " + new_hashes[file]["timestamp"])

    for file in existing_hashes:
        if file not in new_hashes:
            changes["deleted"].append(file + " deleted at " + time.ctime())

    for file in new_hashes:
        if file not in existing_hashes:
            changes["added"].append(file + " added at " + new_hashes[file]["timestamp"])

    with open("changes.json", "w") as f:
        json.dump(changes, f, indent=4)

    with open("baseline.json", "w") as f:
        json.dump(new_hashes, f, indent=4)

    time.sleep(10)