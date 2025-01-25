CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    disaster VARCHAR(255) NOT NULL,
    content TEXT,
    city VARCHAR(255) NOT NULL,
    province VARCHAR(255) NOT NULL,
    curr_time date
);