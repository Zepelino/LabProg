import json


RECORDS_FILE = "src/records.json"


def load_records():
    try:
        with open(RECORDS_FILE, "r") as file:
            records = json.load(file) 
            records.sort(key=lambda x: x["score"], reverse=True)
            return records
    except FileNotFoundError:
        #arquivo não existe
        return []
    except json.JSONDecodeError:
        #arquivo corrompido ou vazio
        return []


def save_records(records):
    with open(RECORDS_FILE, "w") as file:
        json.dump(records, file, indent=4)


def add_or_update_record(name, score):
    records = load_records()
    
    for record in records:
        if record["name"] == name:
            if score > record["score"]:
                record["score"] = score
                save_records(records)
                return True
            return  False
    
    new_id = 0
    for r in records:
        if r["id"] >= new_id:
            new_id = r["id"]+1

    #new_id = records[-1]["id"] + 1 if records else 1
    records.append({"id": new_id, "name": name, "score": score})
    save_records(records)
    return True


def delete_record_by_id(record_id):
    records = load_records()
    # Filtra os recordes, mantendo só os com ID diferente de record_id
    records = [record for record in records if record["id"] != record_id]
    save_records(records)