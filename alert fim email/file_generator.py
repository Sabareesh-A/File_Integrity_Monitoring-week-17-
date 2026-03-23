# CSV file
with open("test.csv", "w") as f:
    f.write("name,age\nAlice,25\nBob,30")

# Shell script (.sh)
with open("script.sh", "w") as f:
    f.write("#!/bin/bash\necho Hello World")

# Markdown file (.md)
with open("README.md", "w") as f:
    f.write("# Test File\nThis is a markdown file.")

# Log file (.log)
with open("app.log", "w") as f:
    f.write("INFO: Application started\nERROR: Something failed")

# passwd-like file
with open("passwd", "w") as f:
    f.write("root:x:0:0:root:/root:/bin/bash")

# shadow-like file
with open("shadow", "w") as f:
    f.write("root:$6$randomhash:19000:0:99999:7:::")

# fake exe file (just for testing)
with open("program.exe", "wb") as f:
    f.write(b"MZ Fake EXE content")