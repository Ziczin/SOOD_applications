import os

for name in os.listdir("."):
    if "orig" in name:
        new_name = name.replace("orig", "")
        if new_name and new_name != name:
            os.rename(name, new_name)
