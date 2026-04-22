# models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class Role(enum.Enum):
    admin = "admin"
    member = "member"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.member)
    joined_at = Column(DateTime, default=datetime.utcnow)
    membership_id = Column(String, unique=True)

    transactions = relationship("Transaction", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    authors = Column(String)   # comma separated authors
    isbn = Column(String, unique=True, nullable=True)
    category = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    shelf = Column(String, nullable=True)
    description = Column(String, nullable=True)

    transactions = relationship("Transaction", back_populates="book")

class TransactionType(enum.Enum):
    issue = "issue"
    return_ = "return"

class TransactionStatus(enum.Enum):
    issued = "issued"
    returned = "returned"
    overdue = "overdue"

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(TransactionType))
    issue_date = Column(DateTime)
    due_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)
    status = Column(Enum(TransactionStatus))
    admin_id = Column(Integer, nullable=True)  # who processed

    book = relationship("Book", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
