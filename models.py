from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class Profile(Base):
    __tablename__ = "profiles"
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    full_name = Column(Text)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Module(Base):
    __tablename__ = "modules"
    id = Column(BigInteger, primary_key=True)
    slug = Column(Text, unique=True)
    title = Column(Text, nullable=True)
    description = Column(Text)
    level = Column(String)
    published = Column(Boolean, default=True)

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(BigInteger, primary_key=True)
    module_id = Column(BigInteger, ForeignKey("modules.id", ondelete="CASCADE"))
    title = Column(Text, nullable=False)
    content_md = Column(Text)
    order_idx = Column(Integer, default=0)

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(BigInteger, primary_key=True)
    lesson_id = Column(BigInteger, ForeignKey("lessons.id", ondelete="CASCADE"))
    title = Column(Text)

class Question(Base):
    __tablename__ = "questions"
    id = Column(BigInteger, primary_key=True)
    quiz_id = Column(BigInteger, ForeignKey("quizzes.id", ondelete="CASCADE"))
    prompt = Column(Text, nullable=False)
    type = Column(String, default="single")

class Option(Base):
    __tablename__ = "options"
    id = Column(BigInteger, primary_key=True)
    question_id = Column(BigInteger, ForeignKey("questions.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(BigInteger, primary_key=True)
    quiz_id = Column(BigInteger, ForeignKey("quizzes.id"))
    user_id = Column(UUID(as_uuid=True))
    score = Column(Numeric(5,2))
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)

class Answer(Base):
    __tablename__ = "answers"
    attempt_id = Column(BigInteger, ForeignKey("attempts.id", ondelete="CASCADE"), primary_key=True)
    question_id = Column(BigInteger, ForeignKey("questions.id"), primary_key=True)
    option_id = Column(BigInteger, ForeignKey("options.id"), primary_key=True)

class Progress(Base):
    __tablename__ = "progress"
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    lesson_id = Column(BigInteger, primary_key=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)

class Badge(Base):
    __tablename__ = "badges"
    id = Column(BigInteger, primary_key=True)
    code = Column(Text, unique=True)
    name = Column(Text)
    description = Column(Text)
    criteria = Column(JSONB)

class UserBadge(Base):
    __tablename__ = "user_badges"
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    badge_id = Column(BigInteger, primary_key=True)
    awarded_at = Column(DateTime, default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(UUID(as_uuid=True))
    kind = Column(Text)
    ref_id = Column(Text)
    at = Column(DateTime, default=datetime.utcnow)
