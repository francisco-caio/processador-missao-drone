import sqlite3
print("Conectando ao banco de dados...")
conexao = sqlite3.connect("dados_drone.db")
cursor = conexao.cursor()

cursor.execute("SELECT *FROM voos")
dados_salvos = cursor.fetchall()

if not dados_salvos:
    print("Nenhum dado encontrado no banco de dados.")
else:
    print(f"Encontrados {len(dados_salvos)} voos no banco:")
    for linha in dados_salvos:
        print(linha)

conexao.close()