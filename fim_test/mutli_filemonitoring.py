import os
import hashlib
import time
import json

folder_path = "/Users/sabareeshanil/Desktop/fim/fim_test/file_dir"
hashes = {}

def process_file(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    file_name = os.path.basename(file_path)
    current_time = time.ctime()

    hashes[file_name] = {
        "hash": file_hash,
        "timestamp": current_time
    }


for file in os.listdir(folder_path):
    full_path = os.path.join(folder_path, file)
    process_file(full_path)




with open("baseline.json", "w") as f:
    json.dump(hashes, f, indent=4)