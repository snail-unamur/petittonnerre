from pydantic import BaseModel, EmailStr, ConfigDict, validator
from datetime import datetime
from typing import Optional, List
from models import ObjectCategory, MaintenanceStatus, ContributionStatus


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    location: Optional[str] = None

class UserCreate(UserBase):
    password: str
    password_confirm: str

    # Ajout de validation sur la longueur du mot de passe
    @validator('password')
    def validate_password(cls, v):
        if len(v.encode('utf-8')) > 72:  # bcrypt limite à 72 bytes
            raise ValueError('Le mot de passe ne peut pas dépasser 72 caractères')
        if len(v) < 8:
            raise ValueError('Le mot de passe doit faire au moins 8 caractères')
        return v

    # Validation que les mots de passe correspondent
    @validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Les mots de passe ne correspondent pas')
        return v

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

# Classe interne pour les opérations internes uniquement, ne pas utiliser comme response_model
class UserInternal(UserResponse):
    hashed_password: str
    
    model_config = {"from_attributes": True}


# Object Schemas
class ObjectBase(BaseModel):
    name: str
    category: ObjectCategory
    brand: Optional[str] = None
    model: Optional[str] = None
    purchase_date: Optional[datetime] = None
    manual_url: Optional[str] = None
    notes: Optional[str] = None
    parent_id: Optional[int] = None

class ObjectCreate(ObjectBase):
    pass

class Object(ObjectBase):
    id: int
    owner_id: int
    created_at: datetime
    children: List['Object'] = []
    
    model_config = ConfigDict(from_attributes=True)


# Maintenance Advice Schemas
class MaintenanceAdviceBase(BaseModel):
    title: str
    description: str
    frequency_days: Optional[int] = None
    category: ObjectCategory

class MaintenanceAdviceCreate(MaintenanceAdviceBase):
    pass

class MaintenanceAdvice(MaintenanceAdviceBase):
    id: int
    is_validated: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Maintenance Task Schemas
class MaintenanceTaskBase(BaseModel):
    scheduled_date: datetime
    notes: Optional[str] = None

class MaintenanceTaskCreate(MaintenanceTaskBase):
    object_id: int
    advice_id: int

class MaintenanceTaskUpdate(BaseModel):
    status: Optional[MaintenanceStatus] = None
    completed_date: Optional[datetime] = None
    notes: Optional[str] = None
    was_successful: Optional[bool] = None
    issues_encountered: Optional[str] = None

class MaintenanceTask(MaintenanceTaskBase):
    id: int
    status: MaintenanceStatus
    completed_date: Optional[datetime]
    was_successful: Optional[bool]
    issues_encountered: Optional[str]
    object_id: int
    user_id: int
    advice_id: int
    
    model_config = ConfigDict(from_attributes=True)


# Contribution Schemas
class ContributionBase(BaseModel):
    title: str
    content: str
    category: ObjectCategory

class ContributionCreate(ContributionBase):
    pass

class ContributionUpdate(BaseModel):
    status: Optional[ContributionStatus] = None

class Contribution(ContributionBase):
    id: int
    status: ContributionStatus
    upvotes: int
    author_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Tag Schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
