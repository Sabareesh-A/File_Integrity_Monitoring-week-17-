import hashlib

# Input text
data = input("Enter text to hash: ")
# Convert to bytes
data_bytes = data.encode()

# Generate SHA-256 hash
hash_object = hashlib.sha256(data_bytes)
hash_value = hash_object.hexdigest()

print("Hash:", hash_value)