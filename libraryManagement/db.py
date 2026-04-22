# # db.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Base, User, Book, Transaction, TransactionType, TransactionStatus, Role
# from datetime import datetime, timedelta
# from passlib.hash import bcrypt_sha256

# import uuid

# # Config
# DATABASE_URL = "sqlite:///library.db"
# FINE_PER_DAY = 5  # ₹5 per day overdue
# MAX_BOOKS_PER_USER = 3

# engine = create_engine(DATABASE_URL, echo=False, future=True)
# SessionLocal = sessionmaker(bind=engine)

# def init_db():
#     """Create DB tables"""
#     Base.metadata.create_all(engine)

# # Password helpers
# def hash_password(plain: str) -> str:
#     return bcrypt.hash(plain)

# def verify_password(plain: str, hashed: str) -> bool:
#     return bcrypt.verify(plain, hashed)

# # User operations
# def create_user(session, name: str, email: str, password: str, role: Role = Role.member):
#     if session.query(User).filter_by(email=email).first():
#         raise ValueError("Email already registered")
#     user = User(
#         name=name,
#         email=email,
#         password_hash=hash_password(password),
#         role=role,
#         membership_id="M" + uuid.uuid4().hex[:6].upper()
#     )
#     session.add(user)
#     session.commit()
#     return user

# def authenticate_user(session, email: str, password: str):
#     user = session.query(User).filter_by(email=email).first()
#     if not user:
#         return None
#     if verify_password(password, user.password_hash):
#         return user
#     return None

# # Book operations
# def add_book(session, title: str, authors, total_copies: int = 1, **kwargs):
#     authors_str = ",".join(authors) if isinstance(authors, (list, tuple)) else (authors or "")
#     book = Book(
#         title=title,
#         authors=authors_str,
#         total_copies=total_copies,
#         available_copies=total_copies,
#         **kwargs
#     )
#     session.add(book)
#     session.commit()
#     return book

# def update_book(session, book_id: int, **fields):
#     book = session.get(Book, book_id)
#     if not book:
#         raise ValueError("Book not found")
#     for k, v in fields.items():
#         if hasattr(book, k):
#             setattr(book, k, v)
#     # Ensure available_copies is not greater than total_copies
#     if book.available_copies > book.total_copies:
#         book.available_copies = book.total_copies
#     session.commit()
#     return book

# def delete_book(session, book_id: int):
#     book = session.get(Book, book_id)
#     if not book:
#         raise ValueError("Book not found")
#     session.delete(book)
#     session.commit()
#     return True

# # Issue / Return
# def issue_book(session, user_id: int, book_id: int, days: int = 14, admin_id: int = None):
#     user = session.get(User, user_id)
#     book = session.get(Book, book_id)
#     if not user:
#         raise ValueError("Invalid user ID")
#     if not book:
#         raise ValueError("Invalid book ID")
#     # count active issues for user
#     active_issues = session.query(Transaction).filter_by(user_id=user_id, status=TransactionStatus.issued).count()
#     if active_issues >= MAX_BOOKS_PER_USER:
#         raise ValueError(f"User has reached max issued books ({MAX_BOOKS_PER_USER})")
#     if book.available_copies <= 0:
#         raise ValueError("No copies available")
#     issue_date = datetime.utcnow()
#     due_date = issue_date + timedelta(days=days)
#     txn = Transaction(
#         book=book,
#         user=user,
#         type=TransactionType.issue,
#         issue_date=issue_date,
#         due_date=due_date,
#         status=TransactionStatus.issued,
#         admin_id=admin_id
#     )
#     book.available_copies -= 1
#     session.add(txn)
#     session.commit()
#     return txn

# def return_book(session, transaction_id: int, admin_id: int = None):
#     txn = session.get(Transaction, transaction_id)
#     if not txn:
#         raise ValueError("Transaction not found")
#     if txn.status != TransactionStatus.issued:
#         raise ValueError("Transaction is not an active issue")
#     txn.return_date = datetime.utcnow()
#     days_overdue = (txn.return_date.date() - txn.due_date.date()).days
#     if days_overdue > 0:
#         txn.status = TransactionStatus.overdue
#     else:
#         txn.status = TransactionStatus.returned
#     txn.admin_id = admin_id
#     # increment available copies
#     book = txn.book
#     book.available_copies += 1
#     session.commit()
#     fine = 0
#     if days_overdue > 0:
#         fine = days_overdue * FINE_PER_DAY
#     return txn, days_overdue if days_overdue > 0 else 0, fine

# # Reporting helpers
# def list_all_books(session):
#     return session.query(Book).all()

# def list_all_users(session):
#     return session.query(User).all()

# def list_transactions(session, limit=100):
#     return session.query(Transaction).order_by(Transaction.issue_date.desc()).limit(limit).all()

# def get_user_active_issues(session, user_id: int):
#     return session.query(Transaction).filter_by(user_id=user_id, status=TransactionStatus.issued).all()
