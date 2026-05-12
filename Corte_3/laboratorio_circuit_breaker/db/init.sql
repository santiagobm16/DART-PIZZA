USE app_db;

CREATE TABLE IF NOT EXISTS mascotas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  tipo VARCHAR(255) NOT NULL
);

INSERT INTO mascotas (nombre, tipo) VALUES
  ('Luna', 'perro'),
  ('Michi', 'gato');
