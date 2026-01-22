import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from rich.console import Console
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
    console.print("[bold red]Bem-vindo ao YouTube MP3 Downloader[/bold red]")
    console.print("[bold cyan]Baixe músicas direto do YouTube[/bold cyan]\n")

def url_youtube_valida(url: str) -> bool:
    return (
        "youtube.com/watch" in url
        or "youtu.be/" in url
    )

def main():
    while True:
        mostrar_header()

        console.print("[bold]Cole o link do YouTube:[/bold] ", end="")
        url = input().strip()

        if not url:
            console.print("\n[bold yellow]Saindo do programa...[/bold yellow]")
            break

        if not url_youtube_valida(url):
            console.print("\n[bold red]URL inválida. Cole um link válido do YouTube.[/bold red]")
            input("\nPressione ENTER para tentar novamente...")
            continue

        qualidade = "192"

        pasta_projeto = os.path.dirname(os.path.abspath(__file__))
        pasta_destino = os.path.join(pasta_projeto, "downloads")
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
                percent_str = d.get("_percent_str", "0%").replace("%", "").strip()
                try:
                    percent = float(percent_str)
                    progress.update(task_id, completed=percent)
                except ValueError:
                    pass
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
            console.print("\n[bold cyan]Iniciando download...[/bold cyan]\n")
            with progress:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            console.print("\n[bold green]Download finalizado![/bold green]")
            console.print(f"[bold cyan]Arquivo salvo em:[/bold cyan] [bold]{pasta_destino}[/bold]")

        except DownloadError as e:
            console.print("\n[bold red]Erro ao baixar o vídeo[/bold red]")
            console.print(f"[yellow]{e}[/yellow]")

        except Exception as e:
            console.print("\n[bold red]Erro inesperado[/bold red]")
            console.print(f"[yellow]{e}[/yellow]")

        console.print("\n[bold yellow]Deseja baixar outra música? (S/N):[/bold yellow] ", end="")
        continuar = input().strip().lower()
        if continuar != "s":
            console.print("\n[bold yellow]Programa encerrado[/bold yellow]")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Programa encerrado pelo usuário.[/bold red]")