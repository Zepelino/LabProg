import json

# Caminho do arquivo onde os recordes serão salvos
RECORDS_FILE = "src/records.json"

# Função para carregar os recordes do arquivo JSON
def load_records():
    try:
        with open(RECORDS_FILE, "r") as file:
            records = json.load(file)  # Carrega os dados do arquivo JSON
            return records
    except FileNotFoundError:
        # Se o arquivo não existir, retorna uma lista vazia
        return []
    except json.JSONDecodeError:
        # Se o arquivo estiver corrompido ou vazio, retorna uma lista vazia
        return []

# Função para salvar os recordes no arquivo JSON
def save_records(records):
    with open(RECORDS_FILE, "w") as file:
        json.dump(records, file, indent=4)  # Salva os dados no arquivo JSON com formatação

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