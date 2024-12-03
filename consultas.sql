Recuperar o perfil de um usuário:
SELECT nome, biografia, localizacao, linkFoto
FROM Usuario
WHERE id = 1;

Listar todos os usuários que são membros de um grupo específico:
USE connectme;
SELECT u.id, u.nome
FROM Usuario u
JOIN Participa p ON u.id = p.Usuario_id
WHERE p.Grupo_id = 2 AND p.stParticipaGrupo = TRUE;

Listar todas as postagens feitas em um grupo específico:
USE connectme;
SELECT p.id, p.texto
FROM Postagem p
JOIN Pertence pt ON p.id = pt.Postagem_id
WHERE pt.Grupo_id = 3;

Buscar os grupos de um usuário específico:
USE connectme;
SELECT g.id, g.stInicio, g.stFim
FROM Grupo g
WHERE g.id IN (
    SELECT p.Grupo_id
    FROM Participa p
    WHERE p.Usuario_id = 1 AND p.stParticipaGrupo = TRUE
);

Contagem de postagens feitas por um usuário específico em um grupo:
USE connectme;
SELECT COUNT(*) AS total_postagens
FROM Postagem p
WHERE p.id IN (
    SELECT pe.Postagem_id
    FROM Pertence pe
    WHERE pe.Grupo_id IN (
        SELECT p1.Grupo_id
        FROM Participa p1
        WHERE p1.Usuario_id = 1
    )
);

Listar os amigos de um usuário específico:
USE ConnectMe;
SELECT u1.id AS Usuario_id, u1.nome AS Usuario, u2.id AS Amigo_id, u2.nome AS Amigo
FROM Usuario u1
JOIN EnviaRecebe er ON u1.id = er.Usuario_id_Envia
JOIN Usuario u2 ON er.Usuario_id_Recebe = u2.id
WHERE u1.id = 1;

Listar postagens com mídias associadas:
USE ConnectMe;
SELECT p.id AS Postagem_id, p.texto AS Postagem, m.link AS Midia
FROM Postagem p
JOIN PossuiMidia pm ON p.id = pm.Postagem_id
JOIN Midia m ON pm.Midia_id = m.id;

Engajamento das 10 postagens mais visualizadas de um grupo:
USE ConnectMe;
SELECT 
    p.id AS Postagem_id,
    p.texto AS Postagem,
    COUNT(v.Usuario_id) AS Total_Visualizacoes
FROM Postagem p
JOIN Pertence pe ON p.id = pe.Postagem_id
JOIN Visualiza v ON p.id = v.Postagem_id
WHERE pe.Grupo_id = 3
  AND p.texto IS NOT NULL
GROUP BY p.id, p.texto
ORDER BY Total_Visualizacoes DESC
LIMIT 10;

Contagem de usuários que participaram de um grupo específico:
USE connectme;
SELECT Grupo_id, COUNT(*) AS total_usuarios
FROM Participa
WHERE stParticipaGrupo = TRUE
GROUP BY Grupo_id
HAVING Grupo_id = 2;

Retornar usuários e as mensagens enviadas em um grupo:
USE ConnectMe;
SELECT u.id AS Usuario_id, u.nome, m.texto AS Mensagem, g.id AS Grupo_id
FROM Usuario u
INNER JOIN Mensagem m ON u.id = m.Usuario_id
INNER JOIN Grupo g ON m.Grupo_id = g.id;

Número de postagens em cada grupo específico:
USE connectme;
SELECT Grupo_id, COUNT(*) AS total_postagens
FROM Pertence
GROUP BY Grupo_id;

Total de postagens feitas em grupos por um usuario específico:
USE ConnectMe;
SELECT u.id AS Usuario_id, u.nome, COUNT(p.id) AS total_postagens
FROM Usuario u
JOIN Participa pa ON u.id = pa.Usuario_id
JOIN Pertence pe ON pa.Grupo_id = pe.Grupo_id
JOIN Postagem p ON p.id = pe.Postagem_id
WHERE pa.stParticipaGrupo = TRUE AND u.id = 1
GROUP BY u.id;


Inserir um novo usuário na tabela Usuario:
INSERT INTO Usuario (id, nome, email, dataNascimento, idade, biografia, localizacao, linkFoto)
VALUES (1, 'João Silva', 'joao.silva@email.com', '1995-05-15', 29, 'Biografia do João', 'São Paulo, SP', 'www.com');

Inserir uma nova postagem na tabela Postagem:
INSERT INTO Postagem (id, tipo, texto, link)
VALUES (1, 'Texto', 'Eu e as migas fazendo o TP3 de IBD.', 'http://linkdotexto.com');
