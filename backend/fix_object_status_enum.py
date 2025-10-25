"""
Script pour corriger l'enum objectstatus en base de données
"""
from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL

def fix_object_status_enum():
    """Corriger l'enum objectstatus pour accepter les bonnes valeurs"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    with engine.connect() as conn:
        # Commencer une transaction
        trans = conn.begin()
        
        try:
            # D'abord, changer temporairement la colonne status en VARCHAR
            print("1. Conversion de la colonne status en VARCHAR...")
            conn.execute(text("ALTER TABLE objects ALTER COLUMN status TYPE VARCHAR USING status::text"))
            
            # Supprimer l'ancien type enum
            print("2. Suppression de l'ancien type enum objectstatus...")
            conn.execute(text("DROP TYPE IF EXISTS objectstatus CASCADE"))
            
            # Créer le nouveau type enum avec les bonnes valeurs
            print("3. Création du nouveau type enum...")
            conn.execute(text("CREATE TYPE objectstatus AS ENUM ('active', 'inactive', 'archived')"))
            
            # Remettre la colonne en type enum
            print("4. Reconversion de la colonne status en type enum...")
            conn.execute(text("ALTER TABLE objects ALTER COLUMN status TYPE objectstatus USING status::objectstatus"))
            
            # Ajouter une valeur par défaut
            print("5. Ajout de la valeur par défaut...")
            conn.execute(text("ALTER TABLE objects ALTER COLUMN status SET DEFAULT 'active'"))
            
            # Commit de la transaction
            trans.commit()
            print("✅ Migration réussie: l'enum objectstatus a été corrigé")
            
        except Exception as e:
            trans.rollback()
            print(f"❌ Erreur lors de la migration: {e}")
            raise

if __name__ == "__main__":
    fix_object_status_enum()
