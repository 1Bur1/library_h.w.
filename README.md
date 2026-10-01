# School Library Borrowing App

RP05 Software Design - Assignment 1 (Idea 1: School library borrowing app)

## Files
- `Assignment1_Filled_Template.pdf` - the filled template (requirements + modular design)
- `library_app.py` - the Python code that implements the design

## Modules
| Module | Job |
|---|---|
| `Catalog` | keeps the list of books and whether each one is on the shelf |
| `Members` | keeps the list of students allowed to borrow |
| `LoanManager` | applies the borrowing rules (max 3 books, 14-day due date, overdue) |
| `LibraryMenu` | shows the menu to the librarian and prints results |

## How to run
```
python library_app.py          # start the menu
python library_app.py --test   # run the quick tests
```
