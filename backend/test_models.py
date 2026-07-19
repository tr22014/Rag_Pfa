from database.database import SessionLocal
from app.models import User, Collection, Document, RoleEnum, DocumentStatus

db = SessionLocal()

try:
    # 1. Créer un utilisateur
    test_user = User(
        email="test@example.com",
        hashed_password="fake_hash_pour_le_test",
        full_name="Test User",
        role=RoleEnum.admin
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    print(f"✅ Utilisateur créé : {test_user.id} - {test_user.email}")

    # 2. Créer une collection
    test_collection = Collection(
        name="Test Collection",
        description="Une collection de test"
    )
    db.add(test_collection)
    db.commit()
    db.refresh(test_collection)
    print(f"✅ Collection créée : {test_collection.id} - {test_collection.name}")

    # 3. Créer un document lié à l'utilisateur et à la collection
    test_doc = Document(
        filename="test.pdf",
        filepath="/uploads/test.pdf",
        file_type="pdf",
        status=DocumentStatus.pending,
        collection_id=test_collection.id,
        uploaded_by_id=test_user.id
    )
    db.add(test_doc)
    db.commit()
    db.refresh(test_doc)
    print(f"✅ Document créé : {test_doc.id} - {test_doc.filename}")

    # 4. Vérifier les relations (le vrai test !)
    print(f"📄 Document appartient à : {test_doc.uploaded_by.email}")
    print(f"📁 Document dans la collection : {test_doc.collection.name}")
    print(f"📋 Documents de l'utilisateur : {[d.filename for d in test_user.documents]}")

    print("\n🎉 Tous les tests ont réussi !")

except Exception as e:
    print(f"❌ Erreur : {e}")
    db.rollback()

finally:
    db.close()  