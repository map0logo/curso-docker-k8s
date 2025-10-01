-- Script de inicialización de la base de datos
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de ejemplo
INSERT INTO items (name, description, price) VALUES
('Laptop', 'Laptop de alta gama', 999.99),
('Mouse', 'Mouse inalámbrico', 29.99),
('Teclado', 'Teclado mecánico', 79.99)
ON CONFLICT DO NOTHING;