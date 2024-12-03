import mysql.connector
import random
from datetime import datetime, timedelta
import lorem

# Configuração da conexão com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bellezinhababy1!",
    database="connectme"
)

if mydb.is_connected():
    print("Conectado ao banco de dados ConnectMe!")

mycursor = mydb.cursor()

#Recuperar IDs de uma tabela
def fetch_ids(table_name):
    mycursor.execute(f"SELECT id FROM {table_name}")
    return [row[0] for row in mycursor.fetchall()]


num_usuarios = 1000
num_grupos = 100
num_postagens = 500
num_midias = 200
num_mensagens = 1000

#Usuario
print("Inserindo usuários...")
usuarios_validos = fetch_ids("Usuario")
print(f"Usuários inseridos: {len(usuarios_validos)}")

#Grupo
grupos_validos = fetch_ids("Grupo")
print(f"Grupos inseridos: {len(grupos_validos)}")

#Postagem
postagens_validas = fetch_ids("Postagem")
print(f"Postagens inseridas: {len(postagens_validas)}")

#Midia
midias_validas = fetch_ids("Midia")
print(f"Mídias inseridas: {len(midias_validas)}")

#Mensagem
print(f"Mensagens inseridas: {num_mensagens}")

# Populando as tabelas de relacionamento
BATCH_SIZE = 100
batch_values = []

# Inserir usuários e grupos com um número reduzido de iterações
print("Inserindo usuários e grupos...")
for usuario_id in range(1, num_usuarios + 1):
    for grupo_id in range(1, num_grupos + 1):
        if random.random() < 0.6:
            sql = "INSERT INTO Participa (Usuario_id, Grupo_id, stParticipaGrupo) VALUES (%s, %s, %s)"
            val = (usuario_id, grupo_id, random.choice([True, False]))
            mycursor.execute(sql, val)
        if random.random() < 0.4:
            sql = "INSERT INTO Cria (Usuario_id, Grupo_id, stCriaGrupo) VALUES (%s, %s, %s)"
            val = (usuario_id, grupo_id, random.choice([True, False]))
            mycursor.execute(sql, val)
    if usuario_id % BATCH_SIZE == 0:
        mydb.commit()
        print(f"Lote {usuario_id} de usuários inserido.")
        
# Inserção de mensagens e visualizações
for usuario_id in range(1, num_usuarios + 1):
    for postagem_id in range(1, num_postagens + 1):
        if random.random() < 0.1:
            sql = "INSERT INTO Visualiza (Usuario_id, Postagem_id) VALUES (%s, %s)"
            val = (usuario_id, postagem_id)
            mycursor.execute(sql, val)
            
# Inserir dados nas tabelas de relacionamento com verificação de duplicados
print("Inserindo dados nas tabelas de relacionamento...")
for usuario_id in range(1, num_usuarios + 1):
    for grupo_id in range(1, num_grupos + 1):
        # Verificar se a combinação já existe na tabela Cria
        mycursor.execute("SELECT 1 FROM Cria WHERE Usuario_id = %s AND Grupo_id = %s", (usuario_id, grupo_id))
        result = mycursor.fetchone()
        if result is None:  # Se a combinação não existe, inserir
            if random.random() < 0.5:
                sql = "INSERT INTO Cria (Usuario_id, Grupo_id, stCriaGrupo) VALUES (%s, %s, %s)"
                val = (usuario_id, grupo_id, random.choice([True, False]))
                mycursor.execute(sql, val)

    # Inserir dados na tabela EnviaRecebe
    for usuario_destino_id in range(1, num_usuarios + 1):
        if usuario_id != usuario_destino_id:  # Não enviar mensagem para si mesmo
            if random.random() < 0.4:  # Ajustando a probabilidade
                sql = "INSERT INTO EnviaRecebe (Usuario_id_Envia, Usuario_id_Recebe, stEnviostRecebe) VALUES (%s, %s, %s)"
                val = (usuario_id, usuario_destino_id, random.choice([True, False]))
                mycursor.execute(sql, val)

    # Inserir dados na tabela Pertence com verificação de duplicados
    for postagem_id in range(1, num_postagens + 1):
        for grupo_id in range(1, num_grupos + 1):
            # Verificar se a combinação já existe na tabela Pertence
            mycursor.execute("SELECT 1 FROM Pertence WHERE Postagem_id = %s AND Grupo_id = %s", (postagem_id, grupo_id))
            result = mycursor.fetchone()
            if result is None:  # Se a combinação não existe, inserir
                if random.random() < 0.4:
                    sql = "INSERT INTO Pertence (Postagem_id, Grupo_id, postagemGrupo) VALUES (%s, %s, %s)"
                    val = (postagem_id, grupo_id, random.choice([True, False]))
                    mycursor.execute(sql, val)

    # Inserir dados na tabela PossuiMidia com verificação de duplicados
    for postagem_id in range(1, num_postagens + 1):
        for midia_id in range(1, num_midias + 1):
            if random.random() < 0.5:
                batch_values.append((postagem_id, midia_id))

                # Se o batch atingir o tamanho, insira no banco de dados
                if len(batch_values) >= BATCH_SIZE:
                    sql = "INSERT IGNORE INTO PossuiMidia (Postagem_id, Midia_id) VALUES (%s, %s)"
                    mycursor.executemany(sql, batch_values)
                    mydb.commit()  # Garantir que os dados sejam commitados no banco
                    print(f"Inseridos {len(batch_values)} registros na tabela PossuiMidia.")
                    batch_values = []  # Limpar o batch após a inserção

    # Commit final para garantir que todos os dados foram salvos
    if batch_values:
        sql = "INSERT IGNORE INTO PossuiMidia (Postagem_id, Midia_id) VALUES (%s, %s)"
        mycursor.executemany(sql, batch_values)
        mydb.commit() 
        print(f"Inseridos {len(batch_values)} registros restantes na tabela PossuiMidia.")

    print("Dados na tabela PossuiMidia inseridos com sucesso!")                

    # Commit em lotes
    if usuario_id % BATCH_SIZE == 0:
        mydb.commit()
        print(f"Lote {usuario_id} de usuários e dados de relacionamento inseridos.")

# Commit final para garantir que todos os dados foram salvos
mydb.commit()

print("Dados nas tabelas de relacionamento inseridos com sucesso!")
print("Dados inseridos com sucesso!")

# Fechando a conexão
mydb.close()