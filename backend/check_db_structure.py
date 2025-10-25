"""
Script pour vérifier la structure de la table objects
"""
from sqlalchemy import create_engine, inspect
from database import SQLALCHEMY_DATABASE_URL

def check_table_structure():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    inspector = inspect(engine)
    
    # Vérifier la structure de la table objects
    if 'objects' in inspector.get_table_names():
        columns = inspector.get_columns('objects')
        print("📋 Structure de la table 'objects':")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            default = f" DEFAULT {col['default']}" if col['default'] else ""
            print(f"  - {col['name']}: {col['type']} {nullable}{default}")
    else:
        print("❌ La table 'objects' n'existe pas")
    
    # Vérifier aussi object_requests
    if 'object_requests' in inspector.get_table_names():
        columns = inspector.get_columns('object_requests')
        print("\n📋 Structure de la table 'object_requests':")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            default = f" DEFAULT {col['default']}" if col['default'] else ""
            print(f"  - {col['name']}: {col['type']} {nullable}{default}")
    else:
        print("\n❌ La table 'object_requests' n'existe pas")

if __name__ == "__main__":
    check_table_structure()
