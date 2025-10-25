"""
Script d'enrichissement des données d'objets pour Petit Tonnerre.

Ce script permet d'enrichir automatiquement les objets avec :
- Des conseils de maintenance par défaut selon la catégorie
- Des tags prédéfinis
- Des fréquences d'entretien recommandées
"""

import logging
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import (
    Base, Object, ObjectCategory, MaintenanceAdvice, 
    Tag, object_tags
)
from datetime import datetime, UTC

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Données d'enrichissement par catégorie
ENRICHMENT_DATA = {
    ObjectCategory.HEATING: {
        "advice": [
            {
                "title": "Contrôle annuel de la chaudière",
                "description": "Faire vérifier la chaudière par un professionnel certifié pour garantir son bon fonctionnement et sa sécurité.",
                "frequency_days": 365
            },
            {
                "title": "Purge des radiateurs",
                "description": "Purger les radiateurs en début de saison de chauffe pour éliminer l'air et optimiser le rendement.",
                "frequency_days": 180
            },
            {
                "title": "Vérification de la pression",
                "description": "Contrôler régulièrement la pression du circuit de chauffage (entre 1 et 1.5 bar à froid).",
                "frequency_days": 30
            }
        ],
        "tags": ["chauffage", "entretien annuel", "sécurité", "professionnel"]
    },
    ObjectCategory.APPLIANCE: {
        "advice": [
            {
                "title": "Nettoyage des filtres",
                "description": "Nettoyer ou remplacer les filtres pour maintenir l'efficacité de l'appareil.",
                "frequency_days": 90
            },
            {
                "title": "Vérification des joints",
                "description": "Contrôler l'état des joints d'étanchéité et les remplacer si nécessaire.",
                "frequency_days": 180
            },
            {
                "title": "Détartrage",
                "description": "Effectuer un détartrage régulier pour les appareils utilisant de l'eau.",
                "frequency_days": 120
            }
        ],
        "tags": ["électroménager", "entretien régulier", "filtres"]
    },
    ObjectCategory.KITCHEN: {
        "advice": [
            {
                "title": "Nettoyage du four",
                "description": "Nettoyer le four en profondeur pour éliminer les graisses et résidus carbonisés.",
                "frequency_days": 30
            },
            {
                "title": "Vérification des joints de porte",
                "description": "Contrôler l'étanchéité de la porte du four pour une cuisson optimale.",
                "frequency_days": 180
            },
            {
                "title": "Nettoyage des brûleurs",
                "description": "Nettoyer les brûleurs à gaz ou les plaques électriques régulièrement.",
                "frequency_days": 14
            }
        ],
        "tags": ["cuisine", "nettoyage", "hygiène"]
    },
    ObjectCategory.BATHROOM: {
        "advice": [
            {
                "title": "Détartrage des robinets",
                "description": "Détartrer les robinets et pommeaux de douche avec du vinaigre blanc.",
                "frequency_days": 90
            },
            {
                "title": "Vérification des joints sanitaires",
                "description": "Inspecter et nettoyer les joints de silicone, remplacer si moisi.",
                "frequency_days": 180
            },
            {
                "title": "Entretien des siphons",
                "description": "Nettoyer les siphons pour éviter les mauvaises odeurs et les bouchons.",
                "frequency_days": 60
            }
        ],
        "tags": ["sanitaire", "détartrage", "hygiène", "plomberie"]
    },
    ObjectCategory.FLOORING: {
        "advice": [
            {
                "title": "Traitement de la pierre bleue",
                "description": "Appliquer un traitement hydrofuge pour protéger la pierre bleue des taches.",
                "frequency_days": 365
            },
            {
                "title": "Nettoyage hebdomadaire",
                "description": "Nettoyer avec un produit adapté au type de sol (pH neutre pour pierre naturelle).",
                "frequency_days": 7
            },
            {
                "title": "Vérification de l'état du joint",
                "description": "Inspecter les joints entre les dalles et refaire si nécessaire.",
                "frequency_days": 365
            }
        ],
        "tags": ["revêtement", "pierre", "protection", "nettoyage"]
    },
    ObjectCategory.OTHER: {
        "advice": [
            {
                "title": "Inspection visuelle régulière",
                "description": "Vérifier visuellement l'état général de l'objet.",
                "frequency_days": 90
            },
            {
                "title": "Nettoyage de base",
                "description": "Effectuer un nettoyage régulier selon les recommandations du fabricant.",
                "frequency_days": 30
            }
        ],
        "tags": ["divers", "entretien général"]
    }
}


def validate_enrichment_data():
    """Valide la cohérence des données d'enrichissement."""
    logger.info("Validation des données d'enrichissement...")
    
    for category, data in ENRICHMENT_DATA.items():
        # Vérifier que chaque catégorie a des conseils
        if not data.get("advice"):
            logger.warning(f"Catégorie {category} sans conseils d'enrichissement")
            return False
        
        # Vérifier que chaque conseil a les champs requis
        for advice in data["advice"]:
            if not all(key in advice for key in ["title", "description", "frequency_days"]):
                logger.error(f"Conseil incomplet pour la catégorie {category}: {advice}")
                return False
            
            # Vérifier que la fréquence est positive
            if advice["frequency_days"] <= 0:
                logger.error(f"Fréquence invalide pour {advice['title']}: {advice['frequency_days']}")
                return False
        
        # Vérifier que la catégorie a des tags
        if not data.get("tags"):
            logger.warning(f"Catégorie {category} sans tags")
    
    logger.info("✓ Validation des données réussie")
    return True


def get_or_create_tag(db: Session, tag_name: str) -> Tag:
    """Récupère un tag existant ou en crée un nouveau."""
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.add(tag)
        db.flush()  # Pour obtenir l'ID
        logger.info(f"✓ Tag créé: {tag_name}")
    return tag


def enrich_object(db: Session, obj: Object) -> dict:
    """
    Enrichit un objet avec des conseils de maintenance et des tags.
    
    Args:
        db: Session de base de données
        obj: L'objet à enrichir
    
    Returns:
        dict: Statistiques de l'enrichissement avec clés:
            - advice_added (int): Nombre de conseils ajoutés
            - tags_added (int): Nombre de tags ajoutés
            - errors (list): Liste des erreurs rencontrées
    
    Raises:
        ValueError: Si l'objet n'a pas de catégorie valide
        SQLAlchemyError: En cas d'erreur de base de données
        Exception: Pour toute autre erreur inattendue
    
    Examples:
        >>> obj = db.query(Object).filter(Object.id == 1).first()
        >>> stats = enrich_object(db, obj)
        >>> print(f"Conseils ajoutés: {stats['advice_added']}")
        Conseils ajoutés: 3
    """
    stats = {
        "advice_added": 0,
        "tags_added": 0,
        "errors": []
    }
    
    try:
        category_data = ENRICHMENT_DATA.get(obj.category)
        if not category_data:
            stats["errors"].append(f"Aucune donnée d'enrichissement pour {obj.category}")
            return stats
        
        # Collecter tous les nouveaux conseils pour bulk insert
        new_advice_list = []
        
        # Enrichir avec des conseils de maintenance
        for advice_data in category_data["advice"]:
            # Vérifier si le conseil existe déjà pour cette catégorie
            existing_advice = db.query(MaintenanceAdvice).filter(
                MaintenanceAdvice.title == advice_data["title"],
                MaintenanceAdvice.category == obj.category
            ).first()
            
            if not existing_advice:
                advice = MaintenanceAdvice(
                    title=advice_data["title"],
                    description=advice_data["description"],
                    frequency_days=advice_data["frequency_days"],
                    category=obj.category,
                    is_validated=True,  # Conseils par défaut sont validés
                    created_at=datetime.now(UTC)
                )
                new_advice_list.append(advice)
                stats["advice_added"] += 1
                logger.debug(f"  + Conseil préparé: {advice_data['title']}")
        
        # Bulk insert des conseils
        if new_advice_list:
            db.bulk_save_objects(new_advice_list)
            logger.debug(f"  ✓ {len(new_advice_list)} conseils insérés en bulk")
        
        # Enrichir avec des tags
        for tag_name in category_data["tags"]:
            tag = get_or_create_tag(db, tag_name)
            
            # Vérifier si le tag n'est pas déjà associé à l'objet
            if tag not in obj.tags:
                obj.tags.append(tag)
                stats["tags_added"] += 1
                logger.debug(f"  + Tag ajouté: {tag_name}")
        
        db.commit()
        logger.info(f"✓ Objet enrichi: {obj.name} ({stats['advice_added']} conseils, {stats['tags_added']} tags)")
        
    except Exception as e:
        db.rollback()
        error_msg = f"Erreur lors de l'enrichissement de {obj.name} (ID: {obj.id}, Catégorie: {obj.category}): {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.exception("Stack trace complet:")
        stats["errors"].append(error_msg)
    
    return stats


def enrich_all_objects(db: Session, category_filter: ObjectCategory = None, force: bool = False):
    """
    Enrichit tous les objets de la base de données.
    
    Args:
        db: Session de base de données
        category_filter: Optionnel, enrichir uniquement une catégorie spécifique
        force: Si True, enrichit même si des données existent déjà
    
    Raises:
        ValueError: Si la validation des données échoue
        SQLAlchemyError: En cas d'erreur de base de données
    
    Examples:
        >>> # Enrichir tous les objets
        >>> db = SessionLocal()
        >>> enrich_all_objects(db)
        
        >>> # Enrichir uniquement les objets de chauffage
        >>> enrich_all_objects(db, category_filter=ObjectCategory.HEATING)
        
        >>> # Forcer l'enrichissement même si déjà fait
        >>> enrich_all_objects(db, force=True)
    """
    logger.info("=" * 60)
    logger.info("Démarrage de l'enrichissement des objets")
    logger.info("=" * 60)
    
    # Validation préalable
    if not validate_enrichment_data():
        logger.error("❌ Échec de la validation des données. Arrêt du script.")
        return
    
    # Vérifier si des données d'enrichissement existent déjà
    if not force:
        existing_advice_count = db.query(MaintenanceAdvice).filter(
            MaintenanceAdvice.is_validated == True
        ).count()
        
        if existing_advice_count > 0:
            logger.info(f"✓ {existing_advice_count} conseils d'enrichissement déjà présents en base.")
            logger.info("Enrichissement ignoré (utiliser force=True pour forcer).")
            return
    
    # Récupérer les objets à enrichir
    query = db.query(Object)
    if category_filter:
        query = query.filter(Object.category == category_filter)
        logger.info(f"Filtre appliqué: catégorie {category_filter}")
    
    objects = query.all()
    logger.info(f"Nombre d'objets à enrichir: {len(objects)}")
    
    if not objects:
        logger.warning("Aucun objet à enrichir dans la base de données.")
        return
    
    # Statistiques globales
    total_stats = {
        "objects_processed": 0,
        "advice_added": 0,
        "tags_added": 0,
        "errors": []
    }
    
    # Enrichir chaque objet
    for obj in objects:
        logger.info(f"\nTraitement: {obj.name} (ID: {obj.id}, Catégorie: {obj.category.value})")
        stats = enrich_object(db, obj)
        
        total_stats["objects_processed"] += 1
        total_stats["advice_added"] += stats["advice_added"]
        total_stats["tags_added"] += stats["tags_added"]
        total_stats["errors"].extend(stats["errors"])
    
    # Résumé final
    logger.info("\n" + "=" * 60)
    logger.info("RÉSUMÉ DE L'ENRICHISSEMENT")
    logger.info("=" * 60)
    logger.info(f"Objets traités: {total_stats['objects_processed']}")
    logger.info(f"Conseils ajoutés: {total_stats['advice_added']}")
    logger.info(f"Tags ajoutés: {total_stats['tags_added']}")
    
    if total_stats["errors"]:
        logger.warning(f"Erreurs rencontrées: {len(total_stats['errors'])}")
        for error in total_stats["errors"]:
            logger.warning(f"  - {error}")
    else:
        logger.info("✓ Aucune erreur rencontrée")
    
    logger.info("=" * 60)


def auto_enrich_on_startup(db: Session):
    """
    Fonction d'enrichissement automatique au démarrage de l'application.
    Enrichit uniquement si aucune donnée d'enrichissement n'existe.
    
    Cette fonction est appelée automatiquement lors du démarrage de FastAPI
    dans main.py pour initialiser la base de données avec des objets et 
    conseils de base.
    
    Args:
        db: Session de base de données
    
    Raises:
        SQLAlchemyError: En cas d'erreur de base de données
        Exception: Pour toute autre erreur lors de la création des objets
    
    Examples:
        >>> # Appelé automatiquement au démarrage de FastAPI
        >>> db = SessionLocal()
        >>> try:
        ...     auto_enrich_on_startup(db)
        ... finally:
        ...     db.close()
    """
    logger.info("🔍 Vérification des données d'enrichissement...")
    
    # Vérifier si des conseils d'enrichissement existent déjà
    existing_advice_count = db.query(MaintenanceAdvice).filter(
        MaintenanceAdvice.is_validated == True
    ).count()
    
    if existing_advice_count > 0:
        logger.info(f"✓ Base de données déjà enrichie ({existing_advice_count} conseils)")
        return
    
    logger.info("⚡ Première initialisation détectée - Création des objets de base...")
    
    # Créer un utilisateur admin par défaut s'il n'existe pas
    from models import User, UserRole
    from base_objects_data import BASE_OBJECTS
    
    admin_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
    
    if not admin_user:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        admin_user = User(
            email="admin@petittonnerre.com",
            username="admin",
            hashed_password=pwd_context.hash("Admin123!"),
            role=UserRole.ADMIN,
            is_active=True,
            location="Système"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        logger.info(f"✓ Utilisateur admin créé (ID: {admin_user.id})")
    
    # Créer des objets de base pour chaque catégorie
    created_objects = []
    for obj_data in BASE_OBJECTS:
        obj = Object(
            name=obj_data["name"],
            category=obj_data["category"],
            brand=obj_data.get("brand"),
            model=obj_data.get("model"),
            notes=obj_data.get("notes"),
            owner_id=admin_user.id,
            created_at=datetime.now(UTC)
        )
        db.add(obj)
        created_objects.append(obj)
    
    db.commit()
    logger.info(f"✓ {len(created_objects)} objets de base créés")
    
    # Maintenant enrichir tous les objets
    logger.info("⚡ Lancement de l'enrichissement...")
    enrich_all_objects(db, force=True)
    logger.info("✓ Enrichissement automatique terminé")


def main():
    """Point d'entrée principal du script."""
    # Créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)
    
    # Créer une session
    db = SessionLocal()
    
    try:
        # Enrichir tous les objets
        enrich_all_objects(db)
        
        # Ou enrichir uniquement une catégorie spécifique:
        # enrich_all_objects(db, category_filter=ObjectCategory.HEATING)
        
    finally:
        db.close()
        logger.info("Session de base de données fermée.")


if __name__ == "__main__":
    main()
