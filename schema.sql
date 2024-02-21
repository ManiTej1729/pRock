CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE uploaded_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    image_name VARCHAR(100) NOT NULL,
    image_description TEXT,
    image_path VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE audio_library (
    id INT AUTO_INCREMENT PRIMARY KEY,
    audio_name VARCHAR(100) NOT NULL,
    audio_artist VARCHAR(100),
    audio_genre VARCHAR(50),
    audio_path VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

