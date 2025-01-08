-- tabel carte
CREATE TABLE IF NOT EXISTS carti (
    id int AUTO_INCREMENT PRIMARY KEY,
    nume VARCHAR(255) NOT NULL,
    nr_pagini int NOT NULL,
    gen VARCHAR(255) NOT NULL,
    editura VARCHAR(255) NOT NULL,
    descriere VARCHAR(4000),
    cale_fisier VARCHAR(255),
    cale_poza VARCHAR(255),
    is_disabled BOOLEAN
);

--INSERT INTO carti (nume, nr_pagini, gen, editura, descriere, cale_fisier, cale_poza, is_disabled) VALUES 
--   ("Fire and Blood", 736, "Fantasy", "HarperCollins", "A song of Ice and Fire", "/", "/", 0);

-- tabel autor
CREATE TABLE IF NOT EXISTS autori (
    id int AUTO_INCREMENT PRIMARY KEY,
    nume VARCHAR(255) NOT NULL,
    descriere VARCHAR(4000)
);

--INSERT INTO autori (nume, descriere) VALUES 
--    ("George R.R Martin", "Autor american de fantasy, horror, science fiction.");

-- tabel carte_autor
CREATE TABLE IF NOT EXISTS carte_autor (
    id_carte int,
    id_autor int,
    PRIMARY KEY (id_carte, id_autor),
    FOREIGN KEY (id_carte) REFERENCES carti(id) ON DELETE CASCADE,
    FOREIGN KEY (id_autor) REFERENCES autori(id) ON DELETE CASCADE
);

--INSERT INTO carte_autor (id_carte, id_autor) VALUES 
--    (1, 1);

CREATE TABLE IF NOT EXISTS bookmarks (
    id_carte int PRIMARY KEY,
    pagina_default int,
    pagina_user int,
    FOREIGN KEY (id_carte) REFERENCES carti(id) ON DELETE CASCADE
)