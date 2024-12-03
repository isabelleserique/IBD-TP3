USE ConnectMe;
CREATE TABLE Usuario (
    id INT PRIMARY KEY,
    nome VARCHAR(255),
    email VARCHAR(255),
    dataNascimento DATE,
    idade INT,
    biografia TEXT,
    localizacao VARCHAR(255),
    linkFoto VARCHAR(255)
);

-- Tabela Grupo
CREATE TABLE Grupo (
    id INT PRIMARY KEY,
    stInicio DATETIME,
    stFim DATETIME
);

-- Tabela Postagem
CREATE TABLE Postagem (
    id INT PRIMARY KEY,
    tipo VARCHAR(255),
    texto TEXT,
    link VARCHAR(255)
);

-- Tabela Mensagem
CREATE TABLE Mensagem (
    id INT PRIMARY KEY,
    texto TEXT,
    Usuario_id INT,
    Grupo_id INT,
    FOREIGN KEY (Usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (Grupo_id) REFERENCES Grupo(id)
);

-- Tabela Midia
CREATE TABLE Midia (
    id INT PRIMARY KEY,
    tipo VARCHAR(255),
    link VARCHAR(255)
);

-- Tabela Participa
CREATE TABLE Participa (
    Usuario_id INT,
    Grupo_id INT,
    stParticipaGrupo BOOLEAN,
    PRIMARY KEY (Usuario_id, Grupo_id),
    FOREIGN KEY (Usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (Grupo_id) REFERENCES Grupo(id)
);

-- Tabela Cria
CREATE TABLE Cria (
    Usuario_id INT,
    Grupo_id INT,
    stCriaGrupo BOOLEAN,
    PRIMARY KEY (Usuario_id, Grupo_id),
    FOREIGN KEY (Usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (Grupo_id) REFERENCES Grupo(id)
);

-- Tabela EnviaRecebe
CREATE TABLE EnviaRecebe (
    Usuario_id_Envia INT,
    Usuario_id_Recebe INT,
    stEnviostRecebe BOOLEAN,
    PRIMARY KEY (Usuario_id_Envia, Usuario_id_Recebe),
    FOREIGN KEY (Usuario_id_Envia) REFERENCES Usuario(id),
    FOREIGN KEY (Usuario_id_Recebe) REFERENCES Usuario(id)
);

-- Tabela Pertence
CREATE TABLE Pertence (
    Postagem_id INT,
    Grupo_id INT,
    postagemGrupo BOOLEAN,
    PRIMARY KEY (Postagem_id, Grupo_id),
    FOREIGN KEY (Postagem_id) REFERENCES Postagem(id),
    FOREIGN KEY (Grupo_id) REFERENCES Grupo(id)
);

-- Tabela PossuiMidia
CREATE TABLE PossuiMidia (
    Postagem_id INT,
    Midia_id INT,
    PRIMARY KEY (Postagem_id, Midia_id),
    FOREIGN KEY (Postagem_id) REFERENCES Postagem(id),
    FOREIGN KEY (Midia_id) REFERENCES Midia(id)
);

-- Tabela Visualiza
CREATE TABLE Visualiza (
    Usuario_id INT,
    Postagem_id INT,
    PRIMARY KEY (Usuario_id, Postagem_id),
    FOREIGN KEY (Usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (Postagem_id) REFERENCES Postagem(id)
);