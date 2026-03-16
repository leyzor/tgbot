import json, os

DB_FILE = "data.json"

def load():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"profile": {}, "tags": {}}, f)
    with open(DB_FILE) as f:
        return json.load(f)

def save(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get(key, default=None):
    return load()["profile"].get(key, default)

def set_field(key, value):
    data = load()
    data["profile"][key] = value
    save(data)

def remove_field(key):
    data = load()
    data["profile"].pop(key, None)
    save(data)

# Tags
def get_tag(name):
    return load()["tags"].get(name)

def set_tag(name, content):
    data = load()
    data["tags"][name] = content
    save(data)

def remove_tag(name):
    data = load()
    if name in data["tags"]:
        del data["tags"][name]
        save(data)
        return True
    return False

def list_tags():
    return list(load()["tags"].keys())
