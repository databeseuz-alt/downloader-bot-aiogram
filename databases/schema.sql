-- Users table
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Downloads history table
CREATE TABLE downloads (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    url TEXT,
    file_type TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Settings table (for admin)
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
