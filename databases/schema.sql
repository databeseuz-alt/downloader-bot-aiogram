-- Users table
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    is_blocked BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Downloads history table
CREATE TABLE downloads (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    url TEXT,
    file_type TEXT, -- 'video', 'audio', 'image'
    platform TEXT, -- 'youtube', 'instagram', etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Settings table
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- Insert default settings
INSERT INTO settings (key, value) VALUES ('maintenance_mode', 'false');
INSERT INTO settings (key, value) VALUES ('welcome_text', 'Salom! Menga havola yuboring.');
