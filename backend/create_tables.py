from database.database import Base, engine
from app import models  # important : force l'import de tous les modèles

print("Création des tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables créées avec succès !")