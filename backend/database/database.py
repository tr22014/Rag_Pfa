from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# URL de connexion PostgreSQL
DATABASE_URL = settings.database_url
# Création du moteur
engine = create_engine(DATABASE_URL)

# Fabrique de sessions  
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Classe de base pour les modèles
Base = declarative_base()

def get_db():
    """
    Crée une session de base de données pour chaque requête
    et la ferme automatiquement à la fin.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()