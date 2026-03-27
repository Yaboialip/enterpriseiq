import subprocess, sys, os

if __name__ == "__main__":
    # Seed database on first run
    db_path = "data/database.db"
    if not os.path.exists(db_path):
        print("🌱 Seeding database...")
        subprocess.run([sys.executable, "data/seed_db.py"])

    # Run Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "ui/app.py",
        "--server.port=8080",
        "--server.address=0.0.0.0"
    ])