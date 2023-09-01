import json


def load_db():
    with open('db.json', 'r') as json_file:
        data = json.load(json_file)
        return data


def update_new_obj(data):
    old_data = load_db()
    old_data.update(data)
    with open("db.json", "w") as json_file:
        json.dump(old_data, json_file, indent=4)


def delete_obj(key):
    old_data = load_db()
    if key in old_data:
        del old_data[key]
        with open('db.json', 'w') as json_file:
            json.dump(old_data, json_file, indent=4)
    else:
        print(f"The key '{key}' does not exist in the JSON data.")