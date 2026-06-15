"""SQLAlchemy database models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AgentExecution(Base):
    """Model for agent execution records."""

    __tablename__ = "agent_executions"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(255), index=True, nullable=False)
    tool_name = Column(String(255), index=True, nullable=True)
    inference_time_ms = Column(Float, nullable=False)
    tokens_input = Column(Integer, nullable=False)
    tokens_output = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)  # success, error, timeout
    error_message = Column(String(1000), nullable=True)
    model = Column(String(255), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return (
            f"<AgentExecution(agent_name={self.agent_name}, "
            f"tool_name={self.tool_name}, "
            f"status={self.status})>"
        )


class Agent(Base):
    """Model for registered agents."""

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(1000), nullable=True)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Agent(name={self.name}, is_active={self.is_active})>"


class Tool(Base):
    """Model for agent tools."""

    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Tool(name={self.name}, category={self.category})>"


class APIKey(Base):
    """Model for API authentication keys."""

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<APIKey(name={self.name}, is_active={self.is_active})>"
