"""
Données des objets de base pour l'enrichissement automatique.
115 objets couvrant toutes les catégories.
"""

from models import ObjectCategory

BASE_OBJECTS = [
    # ========== CHAUFFAGE (15 objets) ==========
    {
        "name": "Chaudière à gaz condensation",
        "category": ObjectCategory.HEATING,
        "brand": "Vaillant",
        "model": "ecoTEC plus VCW 346",
        "notes": "Chaudière à condensation mixte (chauffage + eau chaude) - Installation 2020"
    },
    {
        "name": "Chaudière mazout",
        "category": ObjectCategory.HEATING,
        "brand": "Viessmann",
        "model": "Vitodens 200-W",
        "notes": "Chaudière au mazout - Révision annuelle obligatoire - Cuve 2000L"
    },
    {
        "name": "Radiateurs en acier salon",
        "category": ObjectCategory.HEATING,
        "brand": "Radson",
        "model": "Compact",
        "notes": "5 radiateurs type 22 - Purge annuelle recommandée"
    },
    {
        "name": "Radiateurs électriques chambres",
        "category": ObjectCategory.HEATING,
        "brand": "Atlantic",
        "model": "Solius",
        "notes": "3 radiateurs électriques avec thermostat intégré"
    },
    {
        "name": "Pompe à chaleur air-eau",
        "category": ObjectCategory.HEATING,
        "brand": "Daikin",
        "model": "Altherma 3",
        "notes": "PAC basse température - COP 4.5 - Entretien annuel"
    },
    {
        "name": "Chauffe-eau thermodynamique",
        "category": ObjectCategory.HEATING,
        "brand": "Atlantic",
        "model": "Calypso",
        "notes": "200L - Résistance électrique d'appoint - Détartrage tous les 2 ans"
    },
    {
        "name": "Poêle à pellets",
        "category": ObjectCategory.HEATING,
        "brand": "Ravelli",
        "model": "RV 100",
        "notes": "Chauffage d'appoint salon - 10kW - Nettoyage hebdomadaire"
    },
    {
        "name": "Insert cheminée bois",
        "category": ObjectCategory.HEATING,
        "brand": "Godin",
        "model": "Le Cube",
        "notes": "Insert à bûches - Ramonage 2x/an obligatoire"
    },
    {
        "name": "Thermostat connecté",
        "category": ObjectCategory.HEATING,
        "brand": "Nest",
        "model": "Learning Thermostat",
        "notes": "Thermostat intelligent avec programmation - App mobile"
    },
    {
        "name": "Vanne thermostatique radiateurs",
        "category": ObjectCategory.HEATING,
        "brand": "Danfoss",
        "model": "RAE",
        "notes": "8 vannes thermostatiques - Remplacement tous les 10 ans"
    },
    {
        "name": "Circulateur chauffage central",
        "category": ObjectCategory.HEATING,
        "brand": "Grundfos",
        "model": "Alpha2",
        "notes": "Pompe de circulation A+ - Contrôle annuel"
    },
    {
        "name": "Vase d'expansion chauffage",
        "category": ObjectCategory.HEATING,
        "brand": "Reflex",
        "model": "N 25",
        "notes": "25L - Vérification pression annuelle"
    },
    {
        "name": "Ballon tampon",
        "category": ObjectCategory.HEATING,
        "brand": "Flamco",
        "model": "PS 300",
        "notes": "300L - Isolation renforcée - Vidange tous les 5 ans"
    },
    {
        "name": "Plancher chauffant",
        "category": ObjectCategory.HEATING,
        "brand": "Uponor",
        "model": "Siccus",
        "notes": "Système hydraulique 80m² - Température max 45°C"
    },
    {
        "name": "Cuve à mazout enterrée",
        "category": ObjectCategory.HEATING,
        "brand": "Deprez",
        "model": "Double paroi",
        "notes": "3000L - Contrôle étanchéité tous les 5 ans"
    },
    
    # ========== CUISINE (20 objets) ==========
    {
        "name": "Four encastrable pyrolyse",
        "category": ObjectCategory.KITCHEN,
        "brand": "Bosch",
        "model": "HBG635BS1",
        "notes": "Four multifonction avec pyrolyse - Nettoyage automatique haute température"
    },
    {
        "name": "Four vapeur combiné",
        "category": ObjectCategory.KITCHEN,
        "brand": "Miele",
        "model": "DGC 7865",
        "notes": "Four vapeur + chaleur tournante - Détartrage mensuel"
    },
    {
        "name": "Plaque de cuisson induction",
        "category": ObjectCategory.KITCHEN,
        "brand": "Siemens",
        "model": "EH645BE18E",
        "notes": "4 zones induction - Fonction booster - Nettoyage quotidien"
    },
    {
        "name": "Plaque de cuisson gaz",
        "category": ObjectCategory.KITCHEN,
        "brand": "AEG",
        "model": "HG654550SY",
        "notes": "5 feux gaz - Brûleurs fonte - Nettoyage grilles hebdomadaire"
    },
    {
        "name": "Hotte aspirante îlot",
        "category": ObjectCategory.KITCHEN,
        "brand": "Elica",
        "model": "Nikola Tesla",
        "notes": "Hotte à extraction 800m³/h - Filtres charbon à remplacer tous les 6 mois"
    },
    {
        "name": "Hotte murale décorative",
        "category": ObjectCategory.KITCHEN,
        "brand": "Falmec",
        "model": "Mirabilia",
        "notes": "Design avec éclairage LED - Nettoyage filtres métalliques mensuel"
    },
    {
        "name": "Micro-ondes encastrable",
        "category": ObjectCategory.KITCHEN,
        "brand": "Whirlpool",
        "model": "AMW 730",
        "notes": "Micro-ondes + grill - 30L - Nettoyage intérieur hebdomadaire"
    },
    {
        "name": "Cafetière encastrable",
        "category": ObjectCategory.KITCHEN,
        "brand": "Miele",
        "model": "CVA 7845",
        "notes": "Machine à café grains - Détartrage automatique - Nettoyage quotidien"
    },
    {
        "name": "Tiroir chauffant",
        "category": ObjectCategory.KITCHEN,
        "brand": "Bosch",
        "model": "BIC630NS1",
        "notes": "Maintien au chaud - Préchauffage vaisselle"
    },
    {
        "name": "Cave à vin encastrable",
        "category": ObjectCategory.KITCHEN,
        "brand": "Liebherr",
        "model": "WKEes 553",
        "notes": "48 bouteilles - 2 zones température - Filtre charbon annuel"
    },
    {
        "name": "Réfrigérateur armoire",
        "category": ObjectCategory.KITCHEN,
        "brand": "Samsung",
        "model": "RR39M7165S9",
        "notes": "390L - No Frost - Nettoyage trimestriel"
    },
    {
        "name": "Congélateur coffre",
        "category": ObjectCategory.KITCHEN,
        "brand": "Beko",
        "model": "HSA47520",
        "notes": "450L - Dégivrage annuel - Classe énergétique A+"
    },
    {
        "name": "Évier sous-plan granit",
        "category": ObjectCategory.KITCHEN,
        "brand": "Franke",
        "model": "Maris MRG 651",
        "notes": "2 bacs + égouttoir - Matériau composite - Traitement hydrofuge"
    },
    {
        "name": "Robinet mitigeur douchette",
        "category": ObjectCategory.KITCHEN,
        "brand": "Grohe",
        "model": "Minta",
        "notes": "Douchette extractible - Détartrage trimestriel"
    },
    {
        "name": "Plan de travail quartz",
        "category": ObjectCategory.KITCHEN,
        "brand": "Silestone",
        "model": "Lagoon",
        "notes": "3m x 0.65m - Résistant chaleur et rayures - Nettoyage quotidien"
    },
    {
        "name": "Crédence en verre trempé",
        "category": ObjectCategory.KITCHEN,
        "brand": "Securit",
        "model": "Kitchen Glass",
        "notes": "1.5m x 0.6m - Impression numérique - Nettoyage vitres"
    },
    {
        "name": "Éclairage LED sous meubles",
        "category": ObjectCategory.KITCHEN,
        "brand": "Philips",
        "model": "Hue Lightstrip",
        "notes": "Bandeau LED 2m - Contrôle via app - Dépoussiérage mensuel"
    },
    {
        "name": "Robot de cuisine",
        "category": ObjectCategory.KITCHEN,
        "brand": "KitchenAid",
        "model": "Artisan 5KSM175PS",
        "notes": "Robot pâtissier 4.8L - Nettoyage après chaque usage"
    },
    {
        "name": "Blender chauffant",
        "category": ObjectCategory.KITCHEN,
        "brand": "Moulinex",
        "model": "LM924500",
        "notes": "Soup&Co - Nettoyage automatique - Détartrage mensuel"
    },
    {
        "name": "Bouilloire électrique",
        "category": ObjectCategory.KITCHEN,
        "brand": "Bosch",
        "model": "TWK8611",
        "notes": "1.5L - Inox - Détartrage mensuel selon dureté eau"
    },
    
    # ========== ÉLECTROMÉNAGER (25 objets) ==========
    {
        "name": "Lave-vaisselle encastrable",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Miele",
        "model": "G 7310 SCi",
        "notes": "14 couverts - Programme ECO - Sel et liquide de rinçage - Nettoyage filtres hebdomadaire"
    },
    {
        "name": "Lave-vaisselle pose libre",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Bosch",
        "model": "SMS46AW03E",
        "notes": "12 couverts - Classe A++ - Nettoyage bras de lavage mensuel"
    },
    {
        "name": "Machine à laver hublot",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Bosch",
        "model": "WAW28750FG",
        "notes": "9kg - 1400 tours/min - Nettoyage tambour tous les 3 mois - Vérification joints"
    },
    {
        "name": "Machine à laver top",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Whirlpool",
        "model": "TDLR 70220",
        "notes": "7kg - Chargement par le dessus - Détartrage semestriel"
    },
    {
        "name": "Sèche-linge pompe à chaleur",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Samsung",
        "model": "DV90T6240LH",
        "notes": "9kg - Classe A+++ - Nettoyage condenseur mensuel - Vidange bac à eau"
    },
    {
        "name": "Sèche-linge condensation",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Beko",
        "model": "DCU 8230",
        "notes": "8kg - Nettoyage filtres après chaque usage"
    },
    {
        "name": "Lave-linge séchant",
        "category": ObjectCategory.APPLIANCE,
        "brand": "LG",
        "model": "F4DV709H2T",
        "notes": "9kg lavage / 6kg séchage - AI Direct Drive"
    },
    {
        "name": "Réfrigérateur-congélateur américain",
        "category": ObjectCategory.APPLIANCE,
        "brand": "LG",
        "model": "GSL760PZUZ",
        "notes": "601L - Distributeur eau/glaçons - Filtre à eau tous les 6 mois"
    },
    {
        "name": "Réfrigérateur combiné",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Siemens",
        "model": "KG39NXI35",
        "notes": "366L - No Frost - Nettoyage trimestriel"
    },
    {
        "name": "Aspirateur robot",
        "category": ObjectCategory.APPLIANCE,
        "brand": "iRobot",
        "model": "Roomba j7+",
        "notes": "Navigation intelligente - Vidage automatique - Nettoyage brosses hebdomadaire"
    },
    {
        "name": "Aspirateur balai sans fil",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Dyson",
        "model": "V15 Detect",
        "notes": "Batterie 60min - Nettoyage filtres mensuel - Accessoires multiples"
    },
    {
        "name": "Aspirateur traîneau",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Miele",
        "model": "Complete C3",
        "notes": "Sac 4.5L - Filtre HEPA - Changement sac tous les 2 mois"
    },
    {
        "name": "Nettoyeur vapeur",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Kärcher",
        "model": "SC 5 EasyFix",
        "notes": "Réservoir 1.5L - Détartrage tous les 3 mois"
    },
    {
        "name": "Centrale vapeur",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Philips",
        "model": "PerfectCare Elite",
        "notes": "2L - Détartrage automatique - Semelle céramique"
    },
    {
        "name": "Fer à repasser",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Calor",
        "model": "Ultragliss",
        "notes": "Semelle Durilium - Anti-calcaire - Nettoyage mensuel"
    },
    {
        "name": "Ventilateur colonne",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Dyson",
        "model": "Pure Cool TP04",
        "notes": "Purificateur d'air intégré - Filtre à remplacer annuellement"
    },
    {
        "name": "Humidificateur d'air",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Philips",
        "model": "HU4816",
        "notes": "4L - Nettoyage hebdomadaire - Filtre à remplacer tous les 3 mois"
    },
    {
        "name": "Déshumidificateur",
        "category": ObjectCategory.APPLIANCE,
        "brand": "DeLonghi",
        "model": "DEX212F",
        "notes": "12L/jour - Vidange bac journalière - Nettoyage filtres"
    },
    {
        "name": "Radiateur soufflant",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Rowenta",
        "model": "SO9420",
        "notes": "Chauffage d'appoint - Thermostat - Dépoussiérage mensuel"
    },
    {
        "name": "Purificateur d'air",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Xiaomi",
        "model": "Mi Air Purifier 3H",
        "notes": "Filtre HEPA - Remplacement tous les 6 mois"
    },
    {
        "name": "Télévision LED salon",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Samsung",
        "model": "UE65AU7105",
        "notes": "65 pouces 4K - Smart TV - Dépoussiérage écran"
    },
    {
        "name": "Barre de son",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Sonos",
        "model": "Arc",
        "notes": "Dolby Atmos - Wifi - Dépoussiérage grilles"
    },
    {
        "name": "Box internet fibre",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Proximus",
        "model": "Bbox3",
        "notes": "Routeur WiFi 6 - Redémarrage mensuel recommandé"
    },
    {
        "name": "Imprimante multifonction",
        "category": ObjectCategory.APPLIANCE,
        "brand": "HP",
        "model": "OfficeJet Pro 9010",
        "notes": "Jet d'encre - Nettoyage têtes d'impression - Cartouches XL"
    },
    {
        "name": "Ordinateur portable",
        "category": ObjectCategory.APPLIANCE,
        "brand": "Dell",
        "model": "XPS 15",
        "notes": "15 pouces - Nettoyage clavier et écran - Mises à jour système"
    },
    
    # ========== SANITAIRE (18 objets) ==========
    {
        "name": "WC suspendu avec douchette",
        "category": ObjectCategory.BATHROOM,
        "brand": "Geberit",
        "model": "Duofix Sigma",
        "notes": "Système encastré - Vérification mécanisme chasse annuelle - Douchette japonaise"
    },
    {
        "name": "WC au sol classique",
        "category": ObjectCategory.BATHROOM,
        "brand": "Villeroy & Boch",
        "model": "O.novo",
        "notes": "Sortie horizontale - Abattant frein de chute"
    },
    {
        "name": "Cabine de douche complète",
        "category": ObjectCategory.BATHROOM,
        "brand": "Novellini",
        "model": "Glax 3",
        "notes": "120x80cm - Hydromassage - Détartrage jets mensuel"
    },
    {
        "name": "Douche italienne plain-pied",
        "category": ObjectCategory.BATHROOM,
        "brand": "Grohe",
        "model": "Euphoria System 260",
        "notes": "Receveur extra-plat - Colonne thermostatique - Joints à surveiller"
    },
    {
        "name": "Baignoire îlot",
        "category": ObjectCategory.BATHROOM,
        "brand": "Kaldewei",
        "model": "Meisterstück Centro Duo",
        "notes": "180x80cm - Acier émaillé - Nettoyage anti-calcaire hebdomadaire"
    },
    {
        "name": "Baignoire balnéo",
        "category": ObjectCategory.BATHROOM,
        "brand": "Jacuzzi",
        "model": "Aquasoul Offset",
        "notes": "170x75cm - 10 jets - Nettoyage circuit mensuel avec produit spécifique"
    },
    {
        "name": "Lavabo double vasque",
        "category": ObjectCategory.BATHROOM,
        "brand": "Villeroy & Boch",
        "model": "Subway 3.0",
        "notes": "130cm - Céramique - 2 robinets mitigeurs"
    },
    {
        "name": "Vasque à poser",
        "category": ObjectCategory.BATHROOM,
        "brand": "Alape",
        "model": "Unilav",
        "notes": "Ronde 45cm - Acier émaillé - Bonde à clapet"
    },
    {
        "name": "Meuble sous-vasque suspendu",
        "category": ObjectCategory.BATHROOM,
        "brand": "Burgbad",
        "model": "Yumo",
        "notes": "120cm - 2 tiroirs - Laque brillante - Vérification fixations"
    },
    {
        "name": "Miroir LED salle de bain",
        "category": ObjectCategory.BATHROOM,
        "brand": "HIB",
        "model": "Qubic 80",
        "notes": "Éclairage LED intégré - Anti-buée - Nettoyage vitres"
    },
    {
        "name": "Colonne de douche thermostatique",
        "category": ObjectCategory.BATHROOM,
        "brand": "Grohe",
        "model": "Euphoria System 310",
        "notes": "Douchette + tête de douche - Détartrage trimestriel"
    },
    {
        "name": "Robinetterie lavabo cascade",
        "category": ObjectCategory.BATHROOM,
        "brand": "Hansgrohe",
        "model": "PuraVida 110",
        "notes": "Mitigeur design - Détartrage mousseur mensuel"
    },
    {
        "name": "Robinetterie baignoire sur gorge",
        "category": ObjectCategory.BATHROOM,
        "brand": "Axor",
        "model": "Starck",
        "notes": "Thermostatique - Douchette incluse"
    },
    {
        "name": "Sèche-serviettes électrique",
        "category": ObjectCategory.BATHROOM,
        "brand": "Acova",
        "model": "Fassane Premium",
        "notes": "750W - Programmation - Dépoussiérage mensuel"
    },
    {
        "name": "Sèche-serviettes eau chaude",
        "category": ObjectCategory.BATHROOM,
        "brand": "Zehnder",
        "model": "Metropolitan",
        "notes": "Raccordé chauffage central - Purge annuelle"
    },
    {
        "name": "Extracteur d'air hygroréglable",
        "category": ObjectCategory.BATHROOM,
        "brand": "Aldes",
        "model": "Bahia Hygro",
        "notes": "Détection humidité - Nettoyage grille semestriel"
    },
    {
        "name": "Chauffe-eau instantané",
        "category": ObjectCategory.BATHROOM,
        "brand": "Clage",
        "model": "CEX 9",
        "notes": "9kW - Détartrage annuel selon dureté eau"
    },
    {
        "name": "Paroi de douche fixe",
        "category": ObjectCategory.BATHROOM,
        "brand": "Kinedo",
        "model": "Smart Design",
        "notes": "90cm - Verre 8mm - Traitement anti-calcaire"
    },
    
    # ========== REVÊTEMENTS (15 objets) ==========
    {
        "name": "Pierre bleue belge terrasse",
        "category": ObjectCategory.FLOORING,
        "brand": "Carrières du Hainaut",
        "model": "Petit granit scié",
        "notes": "35m² - Traitement hydrofuge annuel - Nettoyage haute pression"
    },
    {
        "name": "Pierre bleue belge intérieur",
        "category": ObjectCategory.FLOORING,
        "brand": "Les Grès du Condroz",
        "model": "Adouci",
        "notes": "Hall d'entrée 12m² - Savon noir hebdomadaire"
    },
    {
        "name": "Parquet massif chêne salon",
        "category": ObjectCategory.FLOORING,
        "brand": "Panaget",
        "model": "Otello 139",
        "notes": "45m² - Huilé naturel - Entretien huile tous les 6 mois"
    },
    {
        "name": "Parquet contrecollé chambres",
        "category": ObjectCategory.FLOORING,
        "brand": "Quick-Step",
        "model": "Palazzo",
        "notes": "60m² - Vernis mat - Nettoyage vapeur interdit"
    },
    {
        "name": "Parquet bambou bureau",
        "category": ObjectCategory.FLOORING,
        "brand": "Moso",
        "model": "Density",
        "notes": "15m² - Écologique - Huilé - Très résistant"
    },
    {
        "name": "Sol vinyle imitation bois",
        "category": ObjectCategory.FLOORING,
        "brand": "Tarkett",
        "model": "Starfloor Click 55",
        "notes": "25m² - Clipsable - Résistant à l'eau - Facile d'entretien"
    },
    {
        "name": "Carrelage grès cérame cuisine",
        "category": ObjectCategory.FLOORING,
        "brand": "Marazzi",
        "model": "Grande Stone Look",
        "notes": "20m² - 120x120cm - Imitation pierre - Joints époxy"
    },
    {
        "name": "Carrelage mosaïque salle de bain",
        "category": ObjectCategory.FLOORING,
        "brand": "Bisazza",
        "model": "Vetricolor",
        "notes": "8m² - Émaux de verre - Nettoyage joints anti-moisissure"
    },
    {
        "name": "Carrelage antidérapant terrasse",
        "category": ObjectCategory.FLOORING,
        "brand": "Cotto d'Este",
        "model": "Kerlite Outdoor",
        "notes": "30m² - R11 antidérapant - Résistant gel"
    },
    {
        "name": "Béton ciré garage",
        "category": ObjectCategory.FLOORING,
        "brand": "Mercadier",
        "model": "Béton ciré",
        "notes": "40m² - Gris anthracite - Re-scellement tous les 2 ans"
    },
    {
        "name": "Tapis berbère salon",
        "category": ObjectCategory.FLOORING,
        "brand": "Beni Ouarain",
        "model": "Artisanal",
        "notes": "3x2m - Laine pure - Aspiration hebdomadaire - Nettoyage pro annuel"
    },
    {
        "name": "Moquette chambres enfants",
        "category": ObjectCategory.FLOORING,
        "brand": "Balsan",
        "model": "Confort",
        "notes": "30m² - Traitement anti-acariens - Aspiration bihebdomadaire"
    },
    {
        "name": "Jonc de mer escalier",
        "category": ObjectCategory.FLOORING,
        "brand": "Sisal",
        "model": "Natural",
        "notes": "15m linéaires - Fibres naturelles - Aspiration minutieuse"
    },
    {
        "name": "Linoléum buanderie",
        "category": ObjectCategory.FLOORING,
        "brand": "Forbo",
        "model": "Marmoleum Click",
        "notes": "10m² - Naturel et écologique - Nettoyage simple"
    },
    {
        "name": "Marbre blanc hall",
        "category": ObjectCategory.FLOORING,
        "brand": "Carrare",
        "model": "Bianco Carrara",
        "notes": "18m² - Poli brillant - Traitement hydrofuge - Très fragile"
    },
    
    # ========== AUTRES (22 objets) ==========
    {
        "name": "Tondeuse à gazon thermique",
        "category": ObjectCategory.OTHER,
        "brand": "Honda",
        "model": "HRX 476",
        "notes": "Autopropulsée 47cm - Vidange huile annuelle - Affûtage lame"
    },
    {
        "name": "Tondeuse robot",
        "category": ObjectCategory.OTHER,
        "brand": "Husqvarna",
        "model": "Automower 305",
        "notes": "600m² - Installation câble périmétrique - Nettoyage lames"
    },
    {
        "name": "Taille-haie électrique",
        "category": ObjectCategory.OTHER,
        "brand": "Bosch",
        "model": "AHS 70-34",
        "notes": "Lame 70cm - Graissage lame après usage"
    },
    {
        "name": "Tronçonneuse thermique",
        "category": ObjectCategory.OTHER,
        "brand": "Stihl",
        "model": "MS 271",
        "notes": "Guide 40cm - Affûtage chaîne régulier - Mélange 2 temps"
    },
    {
        "name": "Souffleur de feuilles",
        "category": ObjectCategory.OTHER,
        "brand": "Makita",
        "model": "DUB363",
        "notes": "2x18V sans fil - Nettoyage filtre mensuel"
    },
    {
        "name": "Nettoyeur haute pression",
        "category": ObjectCategory.OTHER,
        "brand": "Kärcher",
        "model": "K5 Premium Full Control",
        "notes": "145 bars - Détartrage annuel - Protection gel hiver"
    },
    {
        "name": "Climatisation réversible salon",
        "category": ObjectCategory.OTHER,
        "brand": "Daikin",
        "model": "Perfera FTXM50R",
        "notes": "5kW - Split mural - Nettoyage filtres mensuel - Révision annuelle"
    },
    {
        "name": "Climatisation multi-split",
        "category": ObjectCategory.OTHER,
        "brand": "Mitsubishi",
        "model": "MSZ-LN",
        "notes": "3 unités intérieures - 1 groupe extérieur - Contrôle gaz annuel"
    },
    {
        "name": "Adoucisseur d'eau",
        "category": ObjectCategory.OTHER,
        "brand": "Culligan",
        "model": "Evolife",
        "notes": "30L résine - Ajout sel mensuel - Désinfection annuelle"
    },
    {
        "name": "Station de filtration piscine",
        "category": ObjectCategory.OTHER,
        "brand": "Hayward",
        "model": "PowerLine",
        "notes": "Filtre à sable - Nettoyage filtre hebdomadaire - Hivernage"
    },
    {
        "name": "Pompe de relevage cave",
        "category": ObjectCategory.OTHER,
        "brand": "Grundfos",
        "model": "Unilift CC",
        "notes": "Eaux claires - Test fonctionnement mensuel"
    },
    {
        "name": "VMC double flux",
        "category": ObjectCategory.OTHER,
        "brand": "Zehnder",
        "model": "ComfoAir Q",
        "notes": "Ventilation mécanique - Changement filtres tous les 6 mois"
    },
    {
        "name": "Alarme intrusion",
        "category": ObjectCategory.OTHER,
        "brand": "Honeywell",
        "model": "Galaxy Flex",
        "notes": "8 détecteurs - Test mensuel - Batterie backup"
    },
    {
        "name": "Caméras de surveillance",
        "category": ObjectCategory.OTHER,
        "brand": "Hikvision",
        "model": "ColorVu",
        "notes": "4 caméras extérieures - Vision nocturne couleur - Nettoyage objectifs"
    },
    {
        "name": "Sonnette vidéo connectée",
        "category": ObjectCategory.OTHER,
        "brand": "Ring",
        "model": "Video Doorbell Pro",
        "notes": "WiFi - Détection mouvement - Nettoyage objectif"
    },
    {
        "name": "Portail électrique coulissant",
        "category": ObjectCategory.OTHER,
        "brand": "Came",
        "model": "BXV",
        "notes": "4m - Moteur 24V - Graissage rail semestriel"
    },
    {
        "name": "Porte de garage sectionnelle",
        "category": ObjectCategory.OTHER,
        "brand": "Hormann",
        "model": "LPU40",
        "notes": "Motorisation ProMatic - Graissage ressorts annuel"
    },
    {
        "name": "Volets roulants électriques",
        "category": ObjectCategory.OTHER,
        "brand": "Somfy",
        "model": "Oximo RTS",
        "notes": "8 volets - Contrôle sans fil - Nettoyage rails"
    },
    {
        "name": "Store banne motorisé",
        "category": ObjectCategory.OTHER,
        "brand": "Dickson",
        "model": "Orchestra Max",
        "notes": "6x3m - Toile acrylique - Nettoyage annuel - Rentrer si vent"
    },
    {
        "name": "Panneau solaire photovoltaïque",
        "category": ObjectCategory.OTHER,
        "brand": "SunPower",
        "model": "Maxeon 3",
        "notes": "16 panneaux 400W - Onduleur SolarEdge - Nettoyage bisannuel"
    },
    {
        "name": "Ballon eau chaude solaire",
        "category": ObjectCategory.OTHER,
        "brand": "Viessmann",
        "model": "Vitosol 200-T",
        "notes": "300L - 4m² capteurs - Contrôle pression glycol annuel"
    },
    {
        "name": "Borne de recharge véhicule électrique",
        "category": ObjectCategory.OTHER,
        "brand": "Wallbox",
        "model": "Pulsar Plus",
        "notes": "22kW - WiFi - Contrôle via app - Test connexion"
    }
]
