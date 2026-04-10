import requests
import sys
import os
from google import genai
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

load_dotenv()
# Initialize the Rich console for styling
console = Console()
BASE_URL = "http://127.0.0.1:5000"

# Configure Gemini API
# It will now automatically find the key from your .env file
# Configure Gemini API using the new SDK
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
def display_menu():
    console.print("\n")
    console.print(Panel.fit("[bold cyan]📚 Library Management System[/bold cyan]", border_style="cyan"))
    console.print("[1] [bold blue]View all books[/bold blue]")
    console.print("[2] [bold green]Add a new book[/bold green]")
    console.print("[3] [bold yellow]Borrow a book[/bold yellow]")
    console.print("[4] [bold magenta]Return a book[/bold magenta]")
    console.print("[5] [bold purple]Ask AI: What is this book about?[/bold purple]")
    console.print("[6] [bold bright_red]Remove a book[/bold bright_red]") # <-- NEW OPTION
    console.print("[7] [bold red]Exit[/bold red]") # <-- Shifted to 7
    
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

def get_book_summary():
    console.print("\n[bold purple]--- AI Book Summary ---[/bold purple]")
    
    if not GEMINI_API_KEY:
        console.print("\n[bold red]✖ GEMINI_API_KEY environment variable is not set. Please export it to use this feature.[/bold red]")
        return

    book_id = Prompt.ask("Enter the ID of the book you want to know about")
    
    # Fetch the book details to get the title and author for the prompt
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    if response.status_code != 200:
         console.print(f"\n[bold red]✖ {response.json().get('message', 'Book not found.')}[/bold red]")
         return
         
    book = response.json()
    title = book['title']
    author = book['author']

    # Use Rich's status spinner while waiting for the API
# Use Rich's status spinner while waiting for the API
    with console.status(f"[bold purple]Asking Gemini about '{title}'...[/bold purple]", spinner="dots"):
        try:
            if not client:
                console.print("\n[bold red]✖ API Client not initialized. Check your .env file.[/bold red]")
                return

            prompt = f"Provide a concise, engaging summary of the book '{title}' by {author}. Keep it to two paragraphs and use markdown formatting."
            
            # New SDK syntax
            ai_response = client.models.generate_content(
                model='gemini-2.5-flash', # Upgraded to the latest standard model
                contents=prompt
            )
            
            # Render the markdown response inside a styled panel
            console.print("\n")
            console.print(Panel(
                Markdown(ai_response.text), 
                title=f"[bold purple]About: {title}[/bold purple]", 
                border_style="purple"
            ))
            
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
