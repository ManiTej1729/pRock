create table users (
   id INT AUTO_INCREMENT PRIMARY KEY,
   username VARCHAR(50) NOT NULL,
   email VARCHAR(100) NOT NULL,
   password VARCHAR(255) NOT NULL
);

create table uploaded_images (
   id INT AUTO_INCREMENT PRIMARY KEY,
   user_id INT,
   FOREIGN KEY (user_id) REFERENCES users(id),
   image_name VARCHAR(100) NOT NULL,
   fsize FLOAT,
   bindata LONGBLOB,
   upload_date TIMESTAMP
);

create table audio_library (
   id INT AUTO_INCREMENT PRIMARY KEY,
   audio_name VARCHAR(100) NOT NULL,
   duration INT,
   fszie BIGINT,
   bindata LONGBLOB,
   upload_date TIMESTAMP
);
