CREATE TABLE books(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    status VARCHAR(3) NOT NULL,
    user VARCHAR(4) NULL
);
--@block
INSERT INTO books(title, author, status)
VALUES ('title1', 'A.Baker', 'avl'),
    ('title2', 'C.Smith', 'brw'),
    ('title3', 'B.Simons', 'avl'),
    ('title4', 'M.Parker', 'avl'),
    ('title5', 'M.Green', 'brw'),
    ('title123', 'G.Collins', 'avl'),
    ('title500', 'A.King', 'brw');
--@block
CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_id VARCHAR(4) NOT NULL,
    books_amount INT DEFAULT 0
);
--@block
INSERT INTO users(card_id, books_amount)
VALUES ('A123', 3),
    ('C367', 0),
    ('B321', 2),
    ('A987', 6),
    ('H432', 5),
    ('M123', 1),
    ('B777', 4);
--@block