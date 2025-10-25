# Configuration pour mutmut (mutation testing)

def pre_mutation(context):
    """
    Hook appelé avant chaque mutation.
    Permet de filtrer certains fichiers ou mutations.
    """
    # Ignorer les fichiers de migration Alembic
    if 'alembic/' in context.filename:
        context.skip = True
    
    # Ignorer les fichiers de configuration
    if context.filename in ['config.py', 'database.py']:
        context.skip = True
    
    # Ignorer les scripts d'initialisation
    if 'init_data.py' in context.filename or 'enrich_objects.py' in context.filename:
        context.skip = True
