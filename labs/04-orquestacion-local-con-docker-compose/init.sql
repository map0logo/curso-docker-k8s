-- Script de inicialización de la base de datos
CREATE TABLE IF NOT EXISTS example_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO example_data (name) VALUES 
('Tarea de ejemplo 1'),
('Tarea de ejemplo 2')
ON CONFLICT DO NOTHING;