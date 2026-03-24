import requests
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

# Initialize the Rich console for styling
console = Console()
BASE_URL = "http://127.0.0.1:5000"

def display_menu():
    console.print("\n")
    # Creates a neat, bordered panel for the title
    console.print(Panel.fit("[bold cyan]📚 Library Management System[/bold cyan]", border_style="cyan"))
    console.print("[1] [bold blue]View all books[/bold blue]")
    console.print("[2] [bold green]Add a new book[/bold green]")
    console.print("[3] [bold yellow]Borrow a book[/bold yellow]")
    console.print("[4] [bold magenta]Return a book[/bold magenta]")
    console.print("[5] [bold red]Exit[/bold red]")
    
    # Prompt.ask ensures the user only types 1, 2, 3, 4, or 5
    return Prompt.ask("\n[bold]Choose an option[/bold]", choices=["1", "2", "3", "4", "5"])

def view_books():
    try:
        response = requests.get(f"{BASE_URL}/books")
        books = response.json()
        
        if not books:
            console.print("\n[bold yellow]No books available right now.[/bold yellow]")
            return

        # Create a beautiful, auto-formatting table
        table = Table(title="\nCurrent Book Inventory", header_style="bold magenta")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Author", style="blue")
        table.add_column("Status", justify="center")

        for book in books:
            # Color-code the availability status
            status = "[bold red]Borrowed[/bold red]" if book['is_borrowed'] else "[bold green]Available[/bold green]"
            table.add_row(str(book['id']), book['title'], book['author'], status)

        console.print(table)

    except requests.exceptions.ConnectionError:
        console.print("\n[bold white on red] ERROR [/bold white on red] Could not connect to the backend. Is Flask running?")

def add_book():
    console.print("\n[bold green]--- Add a New Book ---[/bold green]")
    title = Prompt.ask("Enter book title")
    author = Prompt.ask("Enter book author")
    
    response = requests.post(f"{BASE_URL}/books", json={"title": title, "author": author})
    console.print(f"\n[bold cyan]✔ {response.json().get('message', 'Error adding book.')}[/bold cyan]")

def borrow_book():
    console.print("\n[bold yellow]--- Borrow a Book ---[/bold yellow]")
    book_id = Prompt.ask("Enter the ID of the book to borrow")
    
    response = requests.put(f"{BASE_URL}/borrow/{book_id}")
    msg = response.json().get('message', 'Error processing request.')
    
    if response.status_code == 200:
        console.print(f"\n[bold green]✔ {msg}[/bold green]")
    else:
        console.print(f"\n[bold red]✖ {msg}[/bold red]")

def return_book():
    console.print("\n[bold magenta]--- Return a Book ---[/bold magenta]")
    book_id = Prompt.ask("Enter the ID of the book to return")
    
    response = requests.put(f"{BASE_URL}/return/{book_id}")
    msg = response.json().get('message', 'Error processing request.')
    
    if response.status_code == 200:
        console.print(f"\n[bold green]✔ {msg}[/bold green]")
    else:
        console.print(f"\n[bold red]✖ {msg}[/bold red]")

def main():
    while True:
        choice = display_menu()
        if choice == '1':
            view_books()
        elif choice == '2':
            add_book()
        elif choice == '3':
            borrow_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            console.print("\n[bold red]Exiting the system. Goodbye![/bold red]\n")
            sys.exit()

if __name__ == "__main__":
    main()
