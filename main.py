import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

console = Console()

def mostrar_header():
    console.clear()
    console.print(
        Panel.fit(
            "[bold red]Bem-vindo ao YouTube MP3 Downloader[/bold red]\n"
            "[cyan]Baixe músicas direto do YouTube[/cyan]",
            border_style="green",
        )
    )

def main():
    mostrar_header()

    url = input("Cole o link do YouTube: ").strip()
    if not url:
        console.print("[bold red]❌ URL inválida.[/bold red]")
        return

    qualidade = "192"

    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    pasta_destino = os.path.join(pasta_projeto, "musicas-baixadas")
    os.makedirs(pasta_destino, exist_ok=True)

    ffmpeg_path = os.path.join(pasta_projeto, "ffmpeg", "ffmpeg.exe")

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.percentage:>3.0f}%"),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    )

    task_id = progress.add_task("Baixando...", total=100)

    def progress_hook(d):
        if d["status"] == "downloading":
            percent = float(d.get("_percent_str", "0%").replace("%", "").strip())
            progress.update(task_id, completed=percent)
        elif d["status"] == "finished":
            progress.update(task_id, completed=100)

    ydl_opts = {
        "format": "bestaudio/best",
        "ffmpeg_location": ffmpeg_path,
        "paths": {"home": pasta_destino},
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": qualidade,
            }
        ],
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": False,
    }

    try:
        console.print("\n[cyan]Iniciando download...[/cyan]\n")
        with progress:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        console.print("\n[bold green] Download finalizado![/bold green]")
        console.print(
            Panel.fit(
                f"[cyan]Arquivo salvo em:[/cyan]\n[bold]{pasta_destino}[/bold]",
                box=box.ROUNDED,
                border_style="green",
            )
        )

    except DownloadError:
        console.print(
            Panel.fit(
                "[bold red]Erro ao baixar o vídeo[/bold red]\n"
                "[yellow]Verifique se o link é válido ou se o vídeo está disponível.[/yellow]",
                border_style="red",
            )
        )

    except FileNotFoundError:
        console.print(
            Panel.fit(
                "[bold red]FFmpeg não encontrado[/bold red]\n"
                "[yellow]Verifique se o ffmpeg.exe está na pasta correta.[/yellow]",
                border_style="red",
            )
        )

    except Exception as e:
        console.print(
            Panel.fit(
                f"[bold red]Erro inesperado[/bold red]\n[yellow]{e}[/yellow]",
                border_style="red",
            )
        )

    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()