import mysql.connector
import random
from datetime import datetime, timedelta
import lorem

# Configuração da conexão com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senha",
    database="connectme"
)

if mydb.is_connected():
    print("Conectado ao banco de dados ConnectMe!")
    
mycursor = mydb.cursor()

# Recuperar IDs de uma tabela
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
for i in range(1, num_usuarios + 1):
    nome = f"Usuario {i}"
    email = f"{nome.lower().replace(' ', '_')}@example.com"
    data_nascimento = datetime.now() - timedelta(days=random.randint(18*365, 60*365))
    idade = (datetime.now() - data_nascimento).days // 365
    biografia = lorem.sentence()
    localizacao = f"Cidade {random.randint(1, 100)}, Estado {random.randint(1, 27)}"
    link_foto = f"https://example.com/fotos/usuario_{i}.jpg"
    sql = """
        INSERT INTO Usuario (id, nome, email, dataNascimento, idade, biografia, localizacao, linkFoto)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    val = (i, nome, email, data_nascimento, idade, biografia, localizacao, link_foto)
    mycursor.execute(sql, val)

usuarios_validos = fetch_ids("Usuario")
print(f"Usuários inseridos: {len(usuarios_validos)}")

#Grupo
print("Inserindo grupos...")
for i in range(1, num_grupos + 1):
    st_inicio = datetime.now() - timedelta(days=random.randint(1, 365))
    st_fim = st_inicio + timedelta(days=random.randint(1, 365))
    sql = "INSERT INTO Grupo (id, stInicio, stFim) VALUES (%s, %s, %s)"
    val = (i, st_inicio, st_fim)
    mycursor.execute(sql, val)

grupos_validos = fetch_ids("Grupo")
print(f"Grupos inseridos: {len(grupos_validos)}")

#Postagem
print("Inserindo postagens...")
for i in range(1, num_postagens + 1):
    tipo = random.choice(["texto", "foto", "video"])
    texto = lorem.paragraph() if tipo == "texto" else None
    link = f"https://example.com/postagens/{i}" if tipo != "texto" else None
    sql = "INSERT INTO Postagem (id, tipo, texto, link) VALUES (%s, %s, %s, %s)"
    val = (i, tipo, texto, link)
    mycursor.execute(sql, val)

postagens_validas = fetch_ids("Postagem")
print(f"Postagens inseridas: {len(postagens_validas)}")

#Midia
print("Inserindo mídias...")
for i in range(1, num_midias + 1):
    tipo = random.choice(["foto", "video"])
    link = f"https://example.com/midia/{i}"
    sql = "INSERT INTO Midia (id, tipo, link) VALUES (%s, %s, %s)"
    val = (i, tipo, link)
    mycursor.execute(sql, val)

midias_validas = fetch_ids("Midia")
print(f"Mídias inseridas: {len(midias_validas)}")

#Mensagem
print("Inserindo mensagens...")
for i in range(1, num_mensagens + 1):
    texto = lorem.sentence()
    usuario_id = random.choice(usuarios_validos)
    grupo_id = random.choice(grupos_validos)
    sql = "INSERT INTO Mensagem (id, texto, Usuario_id, Grupo_id) VALUES (%s, %s, %s, %s)"
    val = (i, texto, usuario_id, grupo_id)
    mycursor.execute(sql, val)

print(f"Mensagens inseridas: {num_mensagens}")

# Confirmando alterações no banco
mydb.commit()
print("Dados inseridos com sucesso!")

# Fechando a conexão
mydb.close()
