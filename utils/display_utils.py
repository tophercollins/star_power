from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def render_star_card_panel(card):
    title = f"[bold cyan]{card.name}[/bold cyan]"

    # Back to 4 vertical rows
    stats_table = Table.grid(padding=(0, 1))
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
        border_style="magenta",
        padding=(1, 2),
        expand=False,
    )
    return panel


def display_card_list(cards, title="Cards in Play"):
    if not cards:
        console.print(f"[dim]{title}: None[/dim]")
        return

    console.print(f"\n[bold underline]{title}[/bold underline]\n")

    # Show each card as a column
    card_table = Table.grid(expand=True)
    for _ in cards:
        card_table.add_column()

    card_table.add_row(*[render_star_card_panel(card) for card in cards])

    console.print(card_table)
