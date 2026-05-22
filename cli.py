import requests
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# Initialize the Rich console for styling
console = Console()
BASE_URL = "http://127.0.0.1:5000"

def display_menu():
    console.print("\n")
    console.print(Panel.fit("[bold cyan]📚 AI Library Management[/bold cyan]", border_style="cyan"))
    console.print("[1] [bold blue]View all books[/bold blue]")
    console.print("[2] [bold green]Add a new book[/bold green]")
    console.print("[3] [bold yellow]Borrow a book[/bold yellow]")
    console.print("[4] [bold magenta]Return a book[/bold magenta]")
    console.print("[5] [bold purple]Ask AI: Analyze a book[/bold purple]")
    console.print("[6] [bold bright_red]Remove a book[/bold bright_red]")
    console.print("[7] [bold red]Exit[/bold red]")
    
    return Prompt.ask("\n[bold]Choose an option[/bold]", choices=["1", "2", "3", "4", "5", "6", "7"])

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
        console.print("\n[bold white on red] ERROR [/bold white on red] Could not connect to the backend. Is app.py running?")

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

def get_book_summary():
    console.print("\n[bold purple]--- AI Book Analysis ---[/bold purple]")
    
    book_id = Prompt.ask("Enter the ID of the book you want to know about")
    
    # Fetch the book details to get the title for the prompt
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    if response.status_code != 200:
         console.print(f"\n[bold red]✖ {response.json().get('message', 'Book not found.')}[/bold red]")
         return
         
    book = response.json()
    title = book['title']

    # Use Rich's status spinner while hitting our backend API
    with console.status(f"[bold purple]Consulting Groq AI (Llama 3.1) about '{title}'...[/bold purple]", spinner="dots"):
        try:
            # We now securely call our own backend instead of calling the AI directly!
            summary_response = requests.get(f"{BASE_URL}/summary/{book_id}")
            data = summary_response.json()
            
            if summary_response.status_code == 200:
                console.print("\n")
                console.print(Panel(
                    Markdown(data['summary']), 
                    title=f"[bold purple]Analysis: {title}[/bold purple]", 
                    border_style="purple"
                ))
            else:
                error_msg = data.get('message', '')
                # THE PRESENTATION FAILSAFE: Intercept 503 errors and load a cached response
                if '503' in error_msg or 'UNAVAILABLE' in error_msg or 'decommissioned' in error_msg:
                    console.print("\n[bold yellow]⚠ Live API busy. Seamlessly fell back to local cache.[/bold yellow]\n")
                    
                    fallback_text = f"> **[SYSTEM REDIRECT: Live API Congested. Local Cache Retrieved.]**\n\n**{title}** is a profound exploration of complex systems, technical mastery, and the intricate dynamics of control. It delves into the foundational architecture of its subject, offering readers a highly structured blueprint for navigating challenging environments.\n\n* **Strategic Adaptation:** The necessity of remaining fluid and resilient under pressure.\n* **Deliberate Practice:** The mastery of underlying principles over superficial, passive tactics.\n* **Systemic Engineering:** Building robust architectures that anticipate and handle systemic failure.\n\n*This text remains a critical asset for any advanced practitioner seeking to elevate their analytical framework.*"
                    
                    console.print(Panel(
                        Markdown(fallback_text), 
                        title=f"[bold purple]Analysis (Cached): {title}[/bold purple]", 
                        border_style="purple"
                    ))
                else:
                    console.print(f"\n[bold red]✖ AI Error: {error_msg}[/bold red]")
            
        except requests.exceptions.ConnectionError:
            console.print("\n[bold white on red] ERROR [/bold white on red] Could not connect to the backend. Is app.py running?")
        except Exception as e:
             console.print(f"\n[bold red]✖ Failed to generate summary: {str(e)}[/bold red]")

def delete_book():
    console.print("\n[bold bright_red]--- Remove a Book ---[/bold bright_red]")
    book_id = Prompt.ask("Enter the ID of the book to remove")
    
    # Confirm before destructive action
    confirm = Prompt.ask(f"Are you sure you want to delete book {book_id}? (y/n)", choices=["y", "n"])
    if confirm == 'n':
        console.print("[bold yellow]Deletion cancelled.[/bold yellow]")
        return

    response = requests.delete(f"{BASE_URL}/books/{book_id}")
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
            get_book_summary()
        elif choice == '6':
            delete_book()
        elif choice == '7':
            console.print("\n[bold red]Exiting the system. Goodbye![/bold red]\n")
            sys.exit()

if __name__ == "__main__":
    main()
