# cli.py
import argparse
from db import (SessionLocal, init_db, create_user, authenticate_user, add_book,
                issue_book, return_book, list_all_books, list_all_users,
                list_transactions, update_book, delete_book)
from models import User, Book, Transaction
from tabulate import tabulate
import sys

def pretty_books(books):
    rows = []
    for b in books:
        rows.append([b.id, b.title, b.authors, b.isbn, b.total_copies, b.available_copies])
    print(tabulate(rows, headers=["ID","Title","Authors","ISBN","Total","Available"], tablefmt="grid"))

def pretty_users(users):
    rows = []
    for u in users:
        rows.append([u.id, u.name, u.email, u.role.value, u.membership_id])
    print(tabulate(rows, headers=["ID","Name","Email","Role","Membership"], tablefmt="grid"))

def pretty_txns(txns):
    rows = []
    for t in txns:
        rows.append([
            t.id,
            t.book.title if t.book else None,
            t.user.name if t.user else None,
            t.type.value,
            t.issue_date.strftime("%Y-%m-%d %H:%M") if t.issue_date else None,
            t.due_date.strftime("%Y-%m-%d %H:%M") if t.due_date else None,
            t.return_date.strftime("%Y-%m-%d %H:%M") if t.return_date else None,
            t.status.value
        ])
    print(tabulate(rows, headers=["TxnID","Book","User","Type","Issue","Due","Return","Status"], tablefmt="grid"))

def require_admin(session, actor_id):
    if actor_id is None:
        raise SystemExit("This action requires --actor-id (admin user id).")
    actor = session.get(User, actor_id)
    if not actor:
        raise SystemExit("Actor user not found.")
    if actor.role.value != "admin":
        raise SystemExit("Actor must be an admin to perform this action.")
    return actor

def main():
    parser = argparse.ArgumentParser(prog="Library CLI")
    parser.add_argument("action", choices=[
        "init",
        "create-user", "login",
        "add-book", "update-book", "delete-book",
        "issue", "return",
        "list-books", "list-users", "list-txns",
        "user-issues"
    ])
    parser.add_argument("--name")
    parser.add_argument("--email")
    parser.add_argument("--password")
    parser.add_argument("--role", choices=["admin","member"], default="member")
    parser.add_argument("--actor-id", type=int, help="ID of acting user (for admin actions)")
    parser.add_argument("--title")
    parser.add_argument("--authors")
    parser.add_argument("--isbn")
    parser.add_argument("--book-id", type=int)
    parser.add_argument("--user-id", type=int)
    parser.add_argument("--txn-id", type=int)
    parser.add_argument("--days", type=int, default=14)
    args = parser.parse_args()

    if args.action == "init":
        init_db()
        print("Database initialized (library.db).")
        return

    session = SessionLocal()

    try:
        if args.action == "create-user":
            if not (args.name and args.email and args.password):
                raise SystemExit("name, email and password are required")
            role = User.__table__.c.role.type.enums if False else args.role  # not used, kept for clarity
            user = create_user(session, args.name, args.email, args.password, role=args.role)
            print(f"Created user: ID={user.id}, name={user.name}, role={user.role.value}, membership={user.membership_id}")

        elif args.action == "login":
            if not (args.email and args.password):
                raise SystemExit("email and password required")
            user = authenticate_user(session, args.email, args.password)
            if not user:
                print("Login failed: invalid credentials")
                return
            print(f"Login success: ID={user.id}, name={user.name}, role={user.role.value}")

        elif args.action == "add-book":
            # require admin
            actor = require_admin(session, args.actor_id)
            if not args.title:
                raise SystemExit("title required")
            authors = args.authors.split(",") if args.authors else ""
            book = add_book(session, args.title, authors, total_copies=1, isbn=args.isbn)
            print(f"Admin {actor.name} added book: ID={book.id}, Title={book.title}")

        elif args.action == "update-book":
            actor = require_admin(session, args.actor_id)
            if not args.book_id:
                raise SystemExit("book-id required")
            fields = {}
            if args.title: fields["title"] = args.title
            if args.authors: fields["authors"] = args.authors
            if args.isbn: fields["isbn"] = args.isbn
            book = update_book(session, args.book_id, **fields)
            print(f"Book updated: ID={book.id}, Title={book.title}")

        elif args.action == "delete-book":
            actor = require_admin(session, args.actor_id)
            if not args.book_id:
                raise SystemExit("book-id required")
            delete_book(session, args.book_id)
            print(f"Book ID {args.book_id} deleted by admin {actor.name}")

        elif args.action == "issue":
            # issuing can be done by admin or librarian; use actor-id optionally (if admin performs)
            if not (args.user_id and args.book_id):
                raise SystemExit("user-id and book-id required")
            admin_id = args.actor_id
            txn = issue_book(session, args.user_id, args.book_id, days=args.days, admin_id=admin_id)
            print(f"Issued: TxnID={txn.id}, BookID={txn.book_id}, UserID={txn.user_id}, Due={txn.due_date}")

        elif args.action == "return":
            if not args.txn_id:
                raise SystemExit("txn-id required")
            admin_id = args.actor_id
            txn, days_overdue, fine = return_book(session, args.txn_id, admin_id=admin_id)
            msg = f"Returned TxnID={txn.id}, status={txn.status.value}."
            if days_overdue > 0:
                msg += f" Overdue by {days_overdue} day(s). Fine: ₹{fine}."
            print(msg)

        elif args.action == "list-books":
            books = list_all_books(session)
            pretty_books(books)

        elif args.action == "list-users":
            users = list_all_users(session)
            pretty_users(users)

        elif args.action == "list-txns":
            txns = list_transactions(session)
            pretty_txns(txns)

        elif args.action == "user-issues":
            if not args.user_id:
                raise SystemExit("user-id required")
            txns = session.query(Transaction).filter_by(user_id=args.user_id).all()
            pretty_txns(txns)

        else:
            print("Unknown action")
    except Exception as e:
        print("Error:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    main()
