from config import db
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB, ENUM

import enum

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    prompts = db.relationship('Prompt', back_populates='user', lazy=True)


class ZendeskTicket(db.Model):
    __tablename__ = 'zendesk_tickets'

    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(), nullable=False)
    ticket_number = db.Column(db.String(), nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    prompts = db.relationship('Prompt', back_populates='zendesk_ticket', lazy=True)


class PromptStatus(enum.Enum):
    PENDING = 'Pending'
    PROCESSED = 'Processed'
    ERROR = 'Error'

status_enum = ENUM(PromptStatus, name="promptstatus", create_type=False)


class Prompt(db.Model):
    __tablename__ = 'prompts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(PromptStatus), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    zd_ticket_id = db.Column(db.Integer, db.ForeignKey('zendesk_tickets.id'), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='prompts')
    zendesk_ticket = db.relationship('ZendeskTicket', back_populates='prompts')
    
    suggested_solutions = db.relationship('SuggestedSolution', back_populates='prompt', lazy=True)
    
    
class SuggestedSolution(db.Model):
    __tablename__ = 'suggested_solutions'

    id = db.Column(db.Integer, primary_key=True)

    prompt_id = db.Column(db.Integer, db.ForeignKey('prompts.id'), nullable=False)
    prompt = db.relationship('Prompt', back_populates='suggested_solutions')

    response_generated = db.Column(db.Boolean, nullable=False, default=False)
    content = db.Column(db.Text)
    supporting_docs = db.Column(JSONB, nullable=False, server_default= '[]')
    feedback_good = db.Column(db.Boolean, nullable=True)
    ai_confidence_score = db.Column(db.Float, nullable=True)
    tokens_used = db.Column(db.Integer, nullable=True)
    processing_time = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))