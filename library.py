


























from datetime import date, timedelta

LOAN_DAYS = 14        
MAX_BOOKS = 3         


class Catalog:
    def __init__(self):

        
        
        self._books = {}

    def add_book(self, book_id, title, author):
        if book_id in self._books:
            return False
        self._books[book_id] = {"title": title, "author": author, "available": True}
        return True











    
    def find_book(self, book_id):
        return self._books.get(book_id)

    def is_available(self, book_id):
        book = self._books.get(book_id)
        return book is not None and book["available"]

    def set_available(self, book_id, available):
        if book_id in self._books:
            self._books[book_id]["available"] = available























    
    def search(self, word):
        word = word.lower()
        results = []
        for book_id, book in self._books.items():
            if word in book["title"].lower() or word in book["author"].lower():
                results.append((book_id, book))
        return results


class Members:
    def __init__(self):
        self._students = {}
    def add_student(self, student_id, name, grade):
        if student_id in self._students:
            return False
        self._students[student_id] = {"name": name, "grade": grade}
        return True





    
    def is_member(self, student_id):
        return student_id in self._students

    def get_name(self, student_id):
        student = self._students.get(student_id)
        return student["name"] if student else None


class LoanManager:

    def __init__(self, catalog, members):
        self.catalog = catalog
        self.members = members
        self._loans = {}

    def _count_loans(self, student_id):
        return sum(1 for loan in self._loans.values() if loan["student_id"] == student_id)

    def borrow(self, student_id, book_id, today=None):
        today = today or date.today()
        if not self.members.is_member(student_id):
            return "Error: student not found."
        if self.catalog.find_book(book_id) is None:
            return "Error: book not found."
        if not self.catalog.is_available(book_id):
            return "Error: book is already borrowed."
        if self._count_loans(student_id) >= MAX_BOOKS:
            return f"Error: student already has {MAX_BOOKS} books."

        due = today + timedelta(days=LOAN_DAYS)
        self._loans[book_id] = {"student_id": student_id, "due": due}
        self.catalog.set_available(book_id, False)
        title = self.catalog.find_book(book_id)["title"]
        return f"OK: '{title}' borrowed. Due back on {due}."

    def return_book(self, book_id, today=None):
        today = today or date.today()
        loan = self._loans.pop(book_id, None)
        if loan is None:
            return "Error: that book is not borrowed."
        self.catalog.set_available(book_id, True)
        if today > loan["due"]:
            days_late = (today - loan["due"]).days
            return f"Returned, but {days_late} day(s) late."
        return "Returned on time. Thanks!"

    def overdue_list(self, today=None):
        today = today or date.today()
        late = []
        for book_id, loan in self._loans.items():
            if today > loan["due"]:
                name = self.members.get_name(loan["student_id"])
                title = self.catalog.find_book(book_id)["title"]
                late.append(f"{name} - '{title}' (due {loan['due']})")
        return late


class LibraryMenu:

    def __init__(self, catalog, members, loans):
        self.catalog = catalog
        self.members = members
        self.loans = loans
    def run(self):
        while True:
            print("\n=== School Library ===")
            print("1. Add book")
            print("2. Add student")
            print("3. Search books")
            print("4. Borrow book")
            print("5. Return book")
            print("6. Show overdue books")
            print("0. Exit")
            choice = input("Choose: ").strip()
            if choice == "1":
                ok = self.catalog.add_book(input("Book ID: "), input("Title: "), input("Author: "))
                print("Book added." if ok else "That book ID already exists.")
            elif choice == "2":
                ok = self.members.add_student(input("Student ID: "), input("Name: "), input("Grade: "))
                print("Student added." if ok else "That student ID already exists.")
            elif choice == "3":
                results = self.catalog.search(input("Search word: "))
                if not results:
                    print("No books found.")
                for book_id, book in results:
                    status = "on shelf" if book["available"] else "borrowed"
                    print(f"[{book_id}] {book['title']} by {book['author']} - {status}")
            elif choice == "4":
                print(self.loans.borrow(input("Student ID: "), input("Book ID: ")))
            elif choice == "5":
                print(self.loans.return_book(input("Book ID: ")))
            elif choice == "6":
                late = self.loans.overdue_list()
                print("No overdue books." if not late else "\n".join(late))
            elif choice == "0":
                print("Bye!")
                break
            else:
                print("Please pick a number from the menu.")


def load_sample_data(catalog, members):
    catalog.add_book("B1", "Harry Potter and the Sorcerer's Stone", "J.K. Rowling")
    catalog.add_book("B2", "The Hunger Games", "Suzanne Collins")
    catalog.add_book("B3", "Wonder", "R.J. Palacio")
    members.add_student("S1", "Ali", "10")
    members.add_student("S2", "Sara", "11")


def run_tests():
    catalog, members = Catalog(), Members()
    load_sample_data(catalog, members)
    loans = LoanManager(catalog, members)
    day1 = date(2026, 10, 1)

    assert loans.borrow("S1", "B1", day1).startswith("OK")
    assert "already borrowed" in loans.borrow("S2", "B1", day1)
    assert "student not found" in loans.borrow("S9", "B2", day1)
    assert loans.borrow("S1", "B2", day1).startswith("OK")
    assert loans.borrow("S1", "B3", day1).startswith("OK")
    catalog.add_book("B4", "Holes", "Louis Sachar")
    assert "already has 3" in loans.borrow("S1", "B4", day1)
    assert len(loans.overdue_list(day1 + timedelta(days=20))) == 3
    assert "late" in loans.return_book("B1", day1 + timedelta(days=16))
    assert catalog.is_available("B1")
    print("All tests passed!")


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        run_tests()
    else:
        catalog, members = Catalog(), Members()
        load_sample_data(catalog, members)
        LibraryMenu(catalog, members, LoanManager(catalog, members)).run()
