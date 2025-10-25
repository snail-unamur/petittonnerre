from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, List
from models import ObjectCategory, MaintenanceStatus, ContributionStatus, ObjectRequestStatus, ProblemStatus, ProblemSeverity, ProblemCategory


# Auth Schemas
class Token(BaseModel):
    """Schéma pour le token JWT"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Données extraites du token"""
    email: str | None = None


class LoginData(BaseModel):
    """Données de connexion"""
    email: EmailStr
    password: str


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    location: Optional[str] = None

class UserCreate(UserBase):
    password: str
    password_confirm: str

    # Ajout de validation sur la longueur du mot de passe (argon2 n'a pas de limite stricte)
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Le mot de passe doit faire au moins 8 caractères')
        return v

    # Validation que les mots de passe correspondent
    @field_validator('password_confirm')
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if 'password' in info.data and v != info.data['password']:
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

class ObjectCreate(ObjectBase):
    pass

class Object(ObjectBase):
    id: int
    created_by: int
    created_at: datetime
    status: Optional[str] = "active"
    
    model_config = ConfigDict(from_attributes=True)

class ObjectWithOwners(Object):
    """Schema with owners list for detailed object view"""
    owner_ids: List[int] = []
    
    model_config = ConfigDict(from_attributes=True)

class ObjectLink(BaseModel):
    """Schema for linking an existing object to a user"""
    object_id: int

class ObjectSearch(BaseModel):
    """Schema for searching objects"""
    name: Optional[str] = None
    category: Optional[ObjectCategory] = None
    brand: Optional[str] = None
    model: Optional[str] = None


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
    name: str
    scheduled_date: datetime
    notes: Optional[str] = None

class MaintenanceTaskCreate(MaintenanceTaskBase):
    object_id: int
    advice_id: int
    status: Optional[MaintenanceStatus] = MaintenanceStatus.PENDING

class MaintenanceTaskUpdate(BaseModel):
    name: Optional[str] = None
    scheduled_date: Optional[datetime] = None
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


# Object Request Schemas
class ObjectRequestBase(BaseModel):
    name: str
    category: ObjectCategory
    brand: Optional[str] = None
    model: Optional[str] = None
    purchase_date: Optional[datetime] = None
    manual_url: Optional[str] = None
    notes: Optional[str] = None

class ObjectRequestCreate(ObjectRequestBase):
    pass

class ObjectRequestResponse(ObjectRequestBase):
    id: int
    status: ObjectRequestStatus
    admin_notes: Optional[str] = None
    requester_id: int
    reviewed_by: Optional[int] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class ObjectRequestDecision(BaseModel):
    status: ObjectRequestStatus  # APPROVED ou REJECTED
    admin_notes: Optional[str] = None


# Problem Schemas
class ProblemBase(BaseModel):
    title: str
    description: str
    category: ProblemCategory
    severity: Optional[ProblemSeverity] = ProblemSeverity.MEDIUM
    symptoms: Optional[str] = None
    possible_causes: Optional[str] = None

class ProblemCreate(ProblemBase):
    object_id: int

class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[ProblemSeverity] = None
    status: Optional[ProblemStatus] = None
    symptoms: Optional[str] = None
    possible_causes: Optional[str] = None

class Problem(ProblemBase):
    id: int
    status: ProblemStatus
    object_id: int
    reported_by: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ProblemResolution Schemas
class ProblemResolutionBase(BaseModel):
    solution: str
    steps: Optional[str] = None
    cost_estimate: Optional[str] = None
    time_estimate: Optional[str] = None
    feedback: Optional[str] = None
    images: Optional[str] = None  # URLs séparées par des virgules

class ProblemResolutionCreate(ProblemResolutionBase):
    problem_id: int

class ProblemResolutionUpdate(BaseModel):
    solution: Optional[str] = None
    steps: Optional[str] = None
    cost_estimate: Optional[str] = None
    time_estimate: Optional[str] = None
    was_successful: Optional[bool] = None
    feedback: Optional[str] = None
    images: Optional[str] = None

class ProblemResolution(ProblemResolutionBase):
    id: int
    problem_id: int
    resolved_by: int
    was_successful: Optional[bool]
    helpfulness_score: int
    images: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
