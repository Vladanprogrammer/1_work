import requests
from rich.console import Console
from rich.panel import Panel
import time

console = Console()

def get_programming_joke():
    # URL відкритого API з айтішними жартами
    url = "https://v2.jokeapi.dev/joke/Programming?type=single"
    
    try:
        response = requests.get(url)
        # Перевіряємо, чи успішно пройшов запит
        if response.status_code == 200:
            joke_text = response.json().get("joke", "Жарт десь загубився :(")
            
            # Виводимо жарт у красивій кольоровій панелі
            panel = Panel(
                f"[bold cyan]{joke_text}[/bold cyan]", 
                title="[bold yellow]Випадковий жарт з API[/bold yellow]", 
                expand=False
            )
            console.print(panel)
        else:
            console.print("[bold red]Помилка: сервер не відповідає.[/bold red]")
            
    except Exception as e:
        console.print(f"[bold red]Щось пішло не так: {e}[/bold red]")

if __name__ == "__main__":
    console.print("[bold magenta]Запуск програми через Poetry...[/bold magenta]")
    
    # Невелика штучна пауза з анімацією завантаження для краси
    with console.status("[bold green]З'єднуємося з сервером...[/bold green]"):
        time.sleep(1.5)
        get_programming_joke()