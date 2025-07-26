from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def display_star_card(card):
    title = f"[bold cyan]{card.name}[/bold cyan]"
    stats_table = Table.grid(padding=(0, 2))
    stats_table.add_column(justify="right")
    stats_table.add_column(justify="left")
    stats_table.add_row("Aura", str(card.aura))
    stats_table.add_row("Talent", str(card.talent))
    stats_table.add_row("Influence", str(card.influence))
    stats_table.add_row("Legacy", str(card.legacy))

    tag_str = ", ".join(card.tags) if card.tags else "None"
    panel = Panel(
        stats_table,
        title=title,
        subtitle=f"[dim]Tags: {tag_str}[/dim]",
        border_style="magenta"
    )

    console.print(panel)


def display_card_list(cards, title="Cards in Play"):
    if not cards:
        console.print(f"[dim]{title}: None[/dim]")
        return
    console.print(f"\n[bold underline]{title}[/bold underline]\n")
    for card in cards:
        display_star_card(card)
