# record_manager.py

# Caminho do arquivo onde os recordes serão salvos
RECORDS_FILE = "records.txt"

# Função para carregar os recordes do arquivo
def load_records():
    try:
        with open(RECORDS_FILE, "r") as file:
            records = []
            for line in file.readlines():
                record_id, name, score = line.strip().split(",")
                records.append({"id": int(record_id), "name": name, "score": int(score)})
            return records
    except FileNotFoundError:
        # Se o arquivo não existir, retorna uma lista vazia
        return []

# Função para salvar os recordes no arquivo
def save_records(records):
    with open(RECORDS_FILE, "w") as file:
        for record in records:
            file.write(f"{record['id']},{record['name']},{record['score']}\n")

# Função para adicionar um novo recorde
def add_record(name, score):
    records = load_records()
    # Gera um ID único (último ID + 1 ou 1 se a lista estiver vazia)
    new_id = records[-1]["id"] + 1 if records else 1
    records.append({"id": new_id, "name": name, "score": score})
    save_records(records)

# Função para deletar um recorde pelo ID
def delete_record_by_id(record_id):
    records = load_records()
    # Filtra os recordes, mantendo apenas aqueles com ID diferente do especificado
    records = [record for record in records if record["id"] != record_id]
    save_records(records)