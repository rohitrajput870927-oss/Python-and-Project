import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Book:
    def __init__(self, book_id: str, title: str, author: str, isbn: str, quantity: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        self.available = quantity

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'quantity': self.quantity,
            'available': self.available
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data['book_id'], data['title'], data['author'], 
                   data['isbn'], data['quantity'])
        book.available = data['available']
        return book


class Member:
    def __init__(self, member_id: str, name: str, email: str, phone: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books: List[str] = []

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'borrowed_books': self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        member = cls(data['member_id'], data['name'], 
                     data['email'], data['phone'])
        member.borrowed_books = data['borrowed_books']
        return member


class Transaction:
    def __init__(self, trans_id: str, member_id: str, book_id: str, 
                 borrow_date: str, due_date: str, return_date: Optional[str] = None):
        self.trans_id = trans_id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date

    def to_dict(self):
        return {
            'trans_id': self.trans_id,
            'member_id': self.member_id,
            'book_id': self.book_id,
            'borrow_date': self.borrow_date,
            'due_date': self.due_date,
            'return_date': self.return_date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['trans_id'], data['member_id'], data['book_id'],
                   data['borrow_date'], data['due_date'], data.get('return_date'))


class LibraryManagementSystem:
    def __init__(self, data_file='library_data.json'):
        self.data_file = data_file
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.transactions: Dict[str, Transaction] = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.books = {k: Book.from_dict(v) for k, v in data.get('books', {}).items()}
                self.members = {k: Member.from_dict(v) for k, v in data.get('members', {}).items()}
                self.transactions = {k: Transaction.from_dict(v) for k, v in data.get('transactions', {}).items()}
        except FileNotFoundError:
            print("No existing data found. Starting fresh.")

    def save_data(self):
        data = {
            'books': {k: v.to_dict() for k, v in self.books.items()},
            'members': {k: v.to_dict() for k, v in self.members.items()},
            'transactions': {k: v.to_dict() for k, v in self.transactions.items()}
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_book(self, book_id: str, title: str, author: str, isbn: str, quantity: int):
        if book_id in self.books:
            print(f"Book with ID {book_id} already exists.")
            return False
        self.books[book_id] = Book(book_id, title, author, isbn, quantity)
        self.save_data()
        print(f"Book '{title}' added successfully.")
        return True

    def add_member(self, member_id: str, name: str, email: str, phone: str):
        if member_id in self.members:
            print(f"Member with ID {member_id} already exists.")
            return False
        self.members[member_id] = Member(member_id, name, email, phone)
        self.save_data()
        print(f"Member '{name}' added successfully.")
        return True

    def borrow_book(self, member_id: str, book_id: str, days: int = 14):
        if member_id not in self.members:
            print("Member not found.")
            return False
        if book_id not in self.books:
            print("Book not found.")
            return False
        
        book = self.books[book_id]
        member = self.members[member_id]
        
        if book.available <= 0:
            print("Book not available.")
            return False
        
        borrow_date = datetime.now().strftime('%Y-%m-%d')
        due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        trans_id = f"T{len(self.transactions) + 1:04d}"
        
        transaction = Transaction(trans_id, member_id, book_id, borrow_date, due_date)
        self.transactions[trans_id] = transaction
        
        book.available -= 1
        member.borrowed_books.append(book_id)
        
        self.save_data()
        print(f"Book '{book.title}' borrowed successfully. Due date: {due_date}")
        return True

    def return_book(self, member_id: str, book_id: str):
        if member_id not in self.members:
            print("Member not found.")
            return False
        if book_id not in self.books:
            print("Book not found.")
            return False
        
        member = self.members[member_id]
        book = self.books[book_id]
        
        if book_id not in member.borrowed_books:
            print("This book was not borrowed by this member.")
            return False
        
        for trans_id, trans in self.transactions.items():
            if (trans.member_id == member_id and trans.book_id == book_id 
                and trans.return_date is None):
                trans.return_date = datetime.now().strftime('%Y-%m-%d')
                book.available += 1
                member.borrowed_books.remove(book_id)
                self.save_data()
                print(f"Book '{book.title}' returned successfully.")
                return True
        
        print("Transaction not found.")
        return False

    def search_books(self, query: str):
        results = []
        query = query.lower()
        for book in self.books.values():
            if (query in book.title.lower() or query in book.author.lower() 
                or query in book.isbn.lower()):
                results.append(book)
        return results

    def display_books(self):
        if not self.books:
            print("No books in the library.")
            return
        print("\n=== Library Books ===")
        for book in self.books.values():
            print(f"ID: {book.book_id} | Title: {book.title} | Author: {book.author}")
            print(f"ISBN: {book.isbn} | Available: {book.available}/{book.quantity}\n")

    def display_members(self):
        if not self.members:
            print("No members registered.")
            return
        print("\n=== Library Members ===")
        for member in self.members.values():
            print(f"ID: {member.member_id} | Name: {member.name}")
            print(f"Email: {member.email} | Phone: {member.phone}")
            print(f"Borrowed Books: {len(member.borrowed_books)}\n")

    def display_transactions(self):
        if not self.transactions:
            print("No transactions recorded.")
            return
        print("\n=== Transactions ===")
        for trans in self.transactions.values():
            status = "Returned" if trans.return_date else "Active"
            print(f"ID: {trans.trans_id} | Member: {trans.member_id} | Book: {trans.book_id}")
            print(f"Borrowed: {trans.borrow_date} | Due: {trans.due_date} | Status: {status}\n")


def main():
    lms = LibraryManagementSystem()
    
    while True:
        print("\n=== Library Management System ===")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Books")
        print("6. Display All Books")
        print("7. Display All Members")
        print("8. Display Transactions")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ")
        
        if choice == '1':
            book_id = input("Book ID: ")
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            quantity = int(input("Quantity: "))
            lms.add_book(book_id, title, author, isbn, quantity)
        
        elif choice == '2':
            member_id = input("Member ID: ")
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            lms.add_member(member_id, name, email, phone)
        
        elif choice == '3':
            member_id = input("Member ID: ")
            book_id = input("Book ID: ")
            days = int(input("Borrow duration (days, default 14): ") or 14)
            lms.borrow_book(member_id, book_id, days)
        
        elif choice == '4':
            member_id = input("Member ID: ")
            book_id = input("Book ID: ")
            lms.return_book(member_id, book_id)
        
        elif choice == '5':
            query = input("Search (title/author/ISBN): ")
            results = lms.search_books(query)
            if results:
                print("\n=== Search Results ===")
                for book in results:
                    print(f"ID: {book.book_id} | Title: {book.title} | Author: {book.author}")
                    print(f"Available: {book.available}/{book.quantity}\n")
            else:
                print("No books found.")
        
        elif choice == '6':
            lms.display_books()
        
        elif choice == '7':
            lms.display_members()
        
        elif choice == '8':
            lms.display_transactions()
        
        elif choice == '9':
            print("Thank you for using the Library Management System!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()