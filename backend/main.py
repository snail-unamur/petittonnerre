from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

security = HTTPBearer()

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# ============= Models =============
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    role: str = "user"  # user or admin
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

class Category(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str

class ObjectTemplate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category_id: str
    maintenance_tips: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ObjectTemplateWithCategory(ObjectTemplate):
    category_name: str

class UserObject(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    template_id: str
    custom_name: str
    purchase_date: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserObjectCreate(BaseModel):
    template_id: str
    custom_name: str
    purchase_date: Optional[str] = None
    notes: Optional[str] = None

class UserObjectWithDetails(UserObject):
    template_name: str
    category_name: str
    maintenance_tips: List[str]

class Proposal(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_id: str
    user_id: str
    proposed_name: Optional[str] = None
    proposed_tips: Optional[List[str]] = None
    comment: Optional[str] = None
    status: str = "pending"  # pending, approved, rejected
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None

class ProposalCreate(BaseModel):
    template_id: str
    proposed_name: Optional[str] = None
    proposed_tips: Optional[List[str]] = None
    comment: Optional[str] = None

class ProposalWithDetails(Proposal):
    template_name: str
    user_email: str

class ProposalValidation(BaseModel):
    status: str  # approved or rejected

# ============= Auth Utilities =============
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = verify_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Utilisateur non authentifié")
        
        user_doc = await db.users.find_one({"id": user_id}, {"_id": 0})
        if not user_doc:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        if isinstance(user_doc.get('created_at'), str):
            user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
        
        return User(**user_doc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token invalide")

async def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return current_user

# ============= Auth Routes =============
@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    # Check if user exists
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    # Hash password
    password_hash = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    user = User(email=user_data.email)
    user_dict = user.model_dump()
    user_dict['password_hash'] = password_hash.decode('utf-8')
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    
    await db.users.insert_one(user_dict)
    
    # Generate token
    token = create_access_token({"user_id": user.id, "email": user.email})
    
    return TokenResponse(access_token=token, user=user)

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    user_doc = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Verify password
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), user_doc['password_hash'].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Convert datetime
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    user = User(**{k: v for k, v in user_doc.items() if k != 'password_hash'})
    
    # Generate token
    token = create_access_token({"user_id": user.id, "email": user.email})
    
    return TokenResponse(access_token=token, user=user)

@api_router.get("/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# ============= Categories Routes =============
@api_router.get("/categories", response_model=List[Category])
async def get_categories():
    categories = await db.categories.find({}, {"_id": 0}).to_list(1000)
    return categories

# ============= Object Templates Routes =============
@api_router.get("/templates", response_model=List[ObjectTemplateWithCategory])
async def get_templates(category_id: Optional[str] = None):
    query = {"category_id": category_id} if category_id else {}
    templates = await db.object_templates.find(query, {"_id": 0}).to_list(1000)
    
    # Enrich with category name
    result = []
    for template in templates:
        if isinstance(template.get('created_at'), str):
            template['created_at'] = datetime.fromisoformat(template['created_at'])
        
        category = await db.categories.find_one({"id": template['category_id']}, {"_id": 0})
        template['category_name'] = category['name'] if category else "Unknown"
        result.append(ObjectTemplateWithCategory(**template))
    
    return result

@api_router.get("/templates/{template_id}", response_model=ObjectTemplateWithCategory)
async def get_template(template_id: str):
    template = await db.object_templates.find_one({"id": template_id}, {"_id": 0})
    if not template:
        raise HTTPException(status_code=404, detail="Template non trouvé")
    
    if isinstance(template.get('created_at'), str):
        template['created_at'] = datetime.fromisoformat(template['created_at'])
    
    category = await db.categories.find_one({"id": template['category_id']}, {"_id": 0})
    template['category_name'] = category['name'] if category else "Unknown"
    
    return ObjectTemplateWithCategory(**template)

# ============= User Objects Routes =============
@api_router.get("/user-objects", response_model=List[UserObjectWithDetails])
async def get_user_objects(current_user: User = Depends(get_current_user)):
    objects = await db.user_objects.find({"user_id": current_user.id}, {"_id": 0}).to_list(1000)
    
    result = []
    for obj in objects:
        if isinstance(obj.get('created_at'), str):
            obj['created_at'] = datetime.fromisoformat(obj['created_at'])
        
        template = await db.object_templates.find_one({"id": obj['template_id']}, {"_id": 0})
        if template:
            category = await db.categories.find_one({"id": template['category_id']}, {"_id": 0})
            obj['template_name'] = template['name']
            obj['category_name'] = category['name'] if category else "Unknown"
            obj['maintenance_tips'] = template['maintenance_tips']
            result.append(UserObjectWithDetails(**obj))
    
    return result

@api_router.get("/user-objects/{object_id}", response_model=UserObjectWithDetails)
async def get_user_object(object_id: str, current_user: User = Depends(get_current_user)):
    obj = await db.user_objects.find_one({"id": object_id, "user_id": current_user.id}, {"_id": 0})
    if not obj:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    
    if isinstance(obj.get('created_at'), str):
        obj['created_at'] = datetime.fromisoformat(obj['created_at'])
    
    template = await db.object_templates.find_one({"id": obj['template_id']}, {"_id": 0})
    if template:
        category = await db.categories.find_one({"id": template['category_id']}, {"_id": 0})
        obj['template_name'] = template['name']
        obj['category_name'] = category['name'] if category else "Unknown"
        obj['maintenance_tips'] = template['maintenance_tips']
    
    return UserObjectWithDetails(**obj)

@api_router.post("/user-objects", response_model=UserObject)
async def create_user_object(obj_data: UserObjectCreate, current_user: User = Depends(get_current_user)):
    # Verify template exists
    template = await db.object_templates.find_one({"id": obj_data.template_id})
    if not template:
        raise HTTPException(status_code=404, detail="Template non trouvé")
    
    user_object = UserObject(
        user_id=current_user.id,
        **obj_data.model_dump()
    )
    
    obj_dict = user_object.model_dump()
    obj_dict['created_at'] = obj_dict['created_at'].isoformat()
    
    await db.user_objects.insert_one(obj_dict)
    
    return user_object

@api_router.delete("/user-objects/{object_id}")
async def delete_user_object(object_id: str, current_user: User = Depends(get_current_user)):
    result = await db.user_objects.delete_one({"id": object_id, "user_id": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    return {"message": "Objet supprimé"}

# ============= Proposals Routes =============
@api_router.get("/proposals", response_model=List[ProposalWithDetails])
async def get_proposals(current_user: User = Depends(get_current_user)):
    proposals = await db.proposals.find({"user_id": current_user.id}, {"_id": 0}).to_list(1000)
    
    result = []
    for proposal in proposals:
        if isinstance(proposal.get('created_at'), str):
            proposal['created_at'] = datetime.fromisoformat(proposal['created_at'])
        if proposal.get('reviewed_at') and isinstance(proposal['reviewed_at'], str):
            proposal['reviewed_at'] = datetime.fromisoformat(proposal['reviewed_at'])
        
        template = await db.object_templates.find_one({"id": proposal['template_id']}, {"_id": 0})
        user = await db.users.find_one({"id": proposal['user_id']}, {"_id": 0})
        
        proposal['template_name'] = template['name'] if template else "Unknown"
        proposal['user_email'] = user['email'] if user else "Unknown"
        
        result.append(ProposalWithDetails(**proposal))
    
    return result

@api_router.post("/proposals", response_model=Proposal)
async def create_proposal(proposal_data: ProposalCreate, current_user: User = Depends(get_current_user)):
    # Verify template exists
    template = await db.object_templates.find_one({"id": proposal_data.template_id})
    if not template:
        raise HTTPException(status_code=404, detail="Template non trouvé")
    
    proposal = Proposal(
        user_id=current_user.id,
        **proposal_data.model_dump()
    )
    
    proposal_dict = proposal.model_dump()
    proposal_dict['created_at'] = proposal_dict['created_at'].isoformat()
    
    await db.proposals.insert_one(proposal_dict)
    
    return proposal

# ============= Admin Routes =============
@api_router.get("/admin/proposals", response_model=List[ProposalWithDetails])
async def get_all_proposals(status_filter: Optional[str] = None, admin: User = Depends(get_admin_user)):
    query = {"status": status_filter} if status_filter else {}
    proposals = await db.proposals.find(query, {"_id": 0}).to_list(1000)
    
    result = []
    for proposal in proposals:
        if isinstance(proposal.get('created_at'), str):
            proposal['created_at'] = datetime.fromisoformat(proposal['created_at'])
        if proposal.get('reviewed_at') and isinstance(proposal['reviewed_at'], str):
            proposal['reviewed_at'] = datetime.fromisoformat(proposal['reviewed_at'])
        
        template = await db.object_templates.find_one({"id": proposal['template_id']}, {"_id": 0})
        user = await db.users.find_one({"id": proposal['user_id']}, {"_id": 0})
        
        proposal['template_name'] = template['name'] if template else "Unknown"
        proposal['user_email'] = user['email'] if user else "Unknown"
        
        result.append(ProposalWithDetails(**proposal))
    
    return result

@api_router.patch("/admin/proposals/{proposal_id}", response_model=Proposal)
async def validate_proposal(proposal_id: str, validation: ProposalValidation, admin: User = Depends(get_admin_user)):
    if validation.status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status invalide")
    
    proposal = await db.proposals.find_one({"id": proposal_id}, {"_id": 0})
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposition non trouvée")
    
    # Update proposal status
    update_data = {
        "status": validation.status,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "reviewed_by": admin.id
    }
    
    await db.proposals.update_one({"id": proposal_id}, {"$set": update_data})
    
    # If approved, update the template
    if validation.status == "approved":
        template_update = {}
        if proposal.get('proposed_name'):
            template_update['name'] = proposal['proposed_name']
        if proposal.get('proposed_tips'):
            template_update['maintenance_tips'] = proposal['proposed_tips']
        
        if template_update:
            await db.object_templates.update_one(
                {"id": proposal['template_id']},
                {"$set": template_update}
            )
    
    # Return updated proposal
    updated_proposal = await db.proposals.find_one({"id": proposal_id}, {"_id": 0})
    if isinstance(updated_proposal.get('created_at'), str):
        updated_proposal['created_at'] = datetime.fromisoformat(updated_proposal['created_at'])
    if updated_proposal.get('reviewed_at') and isinstance(updated_proposal['reviewed_at'], str):
        updated_proposal['reviewed_at'] = datetime.fromisoformat(updated_proposal['reviewed_at'])
    
    return Proposal(**updated_proposal)

# ============= Initialize Data =============
@api_router.post("/admin/init-data")
async def init_data():
    # Check if already initialized
    existing_categories = await db.categories.count_documents({})
    if existing_categories > 0:
        return {"message": "Données déjà initialisées"}
    
    # Create categories
    categories_data = [
        {"id": str(uuid.uuid4()), "name": "Électroménager", "description": "Appareils électriques de la maison"},
        {"id": str(uuid.uuid4()), "name": "Mobilier", "description": "Meubles et ameublement"},
        {"id": str(uuid.uuid4()), "name": "Jardin", "description": "Outils et équipements de jardin"},
        {"id": str(uuid.uuid4()), "name": "Plomberie", "description": "Équipements de plomberie"},
        {"id": str(uuid.uuid4()), "name": "Chauffage", "description": "Systèmes de chauffage"},
        {"id": str(uuid.uuid4()), "name": "Électricité", "description": "Équipements électriques"},
    ]
    await db.categories.insert_many(categories_data)
    
    # Create sample templates
    templates_data = [
        {
            "id": str(uuid.uuid4()),
            "name": "Réfrigérateur",
            "category_id": categories_data[0]['id'],
            "maintenance_tips": [
                "Nettoyer les joints de porte tous les mois",
                "Dégivrer le congélateur tous les 6 mois",
                "Vérifier la température (4°C pour le frigo, -18°C pour le congélateur)",
                "Nettoyer la grille arrière une fois par an"
            ],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Lave-linge",
            "category_id": categories_data[0]['id'],
            "maintenance_tips": [
                "Nettoyer le filtre tous les mois",
                "Détartrer tous les 3 mois avec du vinaigre blanc",
                "Laisser la porte ouverte après utilisation",
                "Vérifier les joints et les nettoyer régulièrement"
            ],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Canapé en tissu",
            "category_id": categories_data[1]['id'],
            "maintenance_tips": [
                "Aspirer toutes les semaines",
                "Nettoyer les taches immédiatement avec un chiffon humide",
                "Utiliser un nettoyant pour tissu tous les 6 mois",
                "Éviter l'exposition directe au soleil"
            ],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Tondeuse à gazon",
            "category_id": categories_data[2]['id'],
            "maintenance_tips": [
                "Nettoyer la lame après chaque utilisation",
                "Affûter les lames tous les ans",
                "Vérifier le niveau d'huile avant chaque utilisation",
                "Hiverner correctement en vidant le carburant"
            ],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Chaudière gaz",
            "category_id": categories_data[4]['id'],
            "maintenance_tips": [
                "Entretien annuel obligatoire par un professionnel",
                "Vérifier la pression (entre 1 et 1.5 bar)",
                "Purger les radiateurs en début de saison",
                "Vérifier l'absence de fuite de gaz régulièrement"
            ],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
    ]
    await db.object_templates.insert_many(templates_data)
    
    return {"message": "Données initialisées avec succès"}

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
