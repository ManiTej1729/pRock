CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE uploaded_images (

    image_name VARCHAR(100) NOT NULL,
    id INT,
    FOREIGN KEY (id) REFERENCES users(id)
);

CREATE TABLE audio_library (
    id INT AUTO_INCREMENT PRIMARY KEY,
    audio_name VARCHAR(100) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

