"""
Database Models for Star Power
SQLAlchemy models for persistence (future implementation)
"""
from sqlalchemy import Column, String, Integer, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # Hashed password
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

class Game(Base):
    """Game model for storing game state"""
    __tablename__ = "games"

    id = Column(String, primary_key=True)
    player1_id = Column(String, ForeignKey("users.id"), nullable=False)
    player2_id = Column(String, ForeignKey("users.id"), nullable=False)

    # Game state stored as JSON (engine.snapshot() output)
    state = Column(JSON, nullable=False)

    # Game metadata
    turn = Column(Integer, default=1)
    status = Column(String(20), default="active")  # active, completed, abandoned
    winner_id = Column(String, ForeignKey("users.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Game(id={self.id}, status={self.status}, turn={self.turn})>"

class Card(Base):
    """Card model for card definitions (migrated from Google Sheets)"""
    __tablename__ = "cards"

    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # star, power, event, fan

    # Card data stored as JSON
    # For StarCard: {aura: int, talent: int, influence: int, legacy: int, tags: [str]}
    # For PowerCard: {stat_modifiers: {stat: modifier}, targets_star: bool}
    # For EventCard: {stat_options: [str], contest_type: str}
    # For FanCard: {bonus: int, tag: str|null}
    data = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Card(id={self.id}, name={self.name}, type={self.type})>"

class GameHistory(Base):
    """Game history for analytics and replay"""
    __tablename__ = "game_history"

    id = Column(String, primary_key=True)
    game_id = Column(String, ForeignKey("games.id"), nullable=False, index=True)
    turn = Column(Integer, nullable=False)

    # Action taken (PLAY_CARD, END_TURN, etc.)
    action = Column(String(50), nullable=False)

    # Action data (command payload)
    data = Column(JSON, nullable=False)

    # State snapshot after action
    state_snapshot = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<GameHistory(game_id={self.game_id}, turn={self.turn}, action={self.action})>"

# TODO: Add migration scripts
# alembic init alembic
# alembic revision --autogenerate -m "Initial schema"
# alembic upgrade head
