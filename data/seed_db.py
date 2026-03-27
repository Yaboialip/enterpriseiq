import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material TEXT NOT NULL,
    quantity REAL NOT NULL,
    unit TEXT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS production (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line TEXT NOT NULL,
    output INTEGER,
    target INTEGER,
    efficiency REAL,
    date TEXT DEFAULT (DATE('now'))
);
CREATE TABLE IF NOT EXISTS machines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT DEFAULT 'Normal',
    temperature REAL,
    last_maintenance TEXT
);
""")

cursor.executescript("""
DELETE FROM inventory; DELETE FROM production; DELETE FROM machines;
INSERT INTO inventory (material, quantity, unit) VALUES
    ('Aluminum', 2450, 'kg'),
    ('Steel Sheet', 1200, 'kg'),
    ('Copper Wire', 380, 'meter'),
    ('Plastic Resin', 650, 'kg'),
    ('Rubber Seal', 1500, 'pcs');
INSERT INTO production (line, output, target, efficiency) VALUES
    ('Line A', 450, 500, 90.0),
    ('Line B', 380, 400, 95.0),
    ('Line C', 210, 250, 84.0);
INSERT INTO machines (name, status, temperature, last_maintenance) VALUES
    ('CNC Machine 1', 'Normal', 65.2, '2026-03-01'),
    ('CNC Machine 2', 'Warning', 88.5, '2026-02-15'),
    ('Assembly Robot 1', 'Normal', 42.1, '2026-03-10'),
    ('Conveyor Belt A', 'Normal', 38.0, '2026-02-28');
""")

conn.commit()
conn.close()
print("✅ Database seeded successfully!")
print(f"📍 Location: {DB_PATH}")