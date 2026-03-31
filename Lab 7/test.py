from rich.console import Console
from rich.panel import Panel
import time

console = Console()

console.print("[bold cyan]Привіт![/bold cyan] Термінал тепер [underline red]кольоровий[/underline red] :sunglasses:")

menu_text = "[green]1.[/green] Камінь\n[green]2.[/green] Ножиці\n[green]3.[/green] Папір"
console.print(Panel(menu_text, title="[bold yellow]Вибір зброї[/bold yellow]", expand=False))

with console.status("[bold magenta]Шукаємо суперника в мережі...[/bold magenta]") as status:
    time.sleep(3) 

console.print("[bold green]Суперника знайдено! Бій починається.[/bold green] :crossed_swords:")