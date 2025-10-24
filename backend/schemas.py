from pydantic import BaseModel, EmailStr, ConfigDict
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

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

class User(UserResponse):
    hashed_password: str


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
    owner_id: int
    created_at: datetime
    
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
