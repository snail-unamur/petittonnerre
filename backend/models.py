from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from database import Base
import enum

class ObjectCategory(str, enum.Enum):
    HEATING = "heating"  # chaudière
    APPLIANCE = "appliance"  # appareils électriques
    KITCHEN = "kitchen"  # four, etc.
    BATHROOM = "bathroom"  # sanitaires
    FLOORING = "flooring"  # pierre bleue, etc.
    OTHER = "other"

class MaintenanceStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    ISSUE_REPORTED = "issue_reported"

class ContributionStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# Table association pour les tags
object_tags = Table(
    'object_tags',
    Base.metadata,
    Column('object_id', Integer, ForeignKey('objects.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    location = Column(String)  # Pour l'aide locale
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relations
    objects = relationship("Object", back_populates="owner")
    maintenance_tasks = relationship("MaintenanceTask", back_populates="user")
    contributions = relationship("Contribution", back_populates="author")


class Object(Base):
    __tablename__ = "objects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(ObjectCategory), nullable=False)
    brand = Column(String)
    model = Column(String)
    purchase_date = Column(DateTime)
    manual_url = Column(String)  # Lien vers le manuel
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Clé étrangère
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relations
    owner = relationship("User", back_populates="objects")
    maintenance_tasks = relationship("MaintenanceTask", back_populates="object")
    maintenance_advice = relationship("MaintenanceAdvice", back_populates="object_type")
    tags = relationship("Tag", secondary=object_tags, back_populates="objects")


class MaintenanceAdvice(Base):
    __tablename__ = "maintenance_advice"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    frequency_days = Column(Integer)  # Fréquence en jours
    category = Column(Enum(ObjectCategory), nullable=False)
    is_validated = Column(Boolean, default=False)  # Validé par la communauté
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Clé étrangère (optionnelle si conseil spécifique à un objet)
    object_type_id = Column(Integer, ForeignKey("objects.id"), nullable=True)
    
    # Relations
    object_type = relationship("Object", back_populates="maintenance_advice")
    maintenance_tasks = relationship("MaintenanceTask", back_populates="advice")


class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    scheduled_date = Column(DateTime, nullable=False)
    completed_date = Column(DateTime)
    status = Column(Enum(MaintenanceStatus), default=MaintenanceStatus.PENDING)
    notes = Column(Text)
    
    # Feedback post-entretien
    was_successful = Column(Boolean)
    issues_encountered = Column(Text)
    
    # Clés étrangères
    object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    advice_id = Column(Integer, ForeignKey("maintenance_advice.id"), nullable=False)
    
    # Relations
    object = relationship("Object", back_populates="maintenance_tasks")
    user = relationship("User", back_populates="maintenance_tasks")
    advice = relationship("MaintenanceAdvice", back_populates="maintenance_tasks")


class Contribution(Base):
    __tablename__ = "contributions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(Enum(ObjectCategory), nullable=False)
    status = Column(Enum(ContributionStatus), default=ContributionStatus.PENDING)
    upvotes = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Clé étrangère
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relations
    author = relationship("User", back_populates="contributions")


class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relations
    objects = relationship("Object", secondary=object_tags, back_populates="tags")
