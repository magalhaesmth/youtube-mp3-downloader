import os
from yt_dlp import YoutubeDL
from rich.console import Console
from rich.panel import Panel
from rich import box

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
        console.print("[red]URL inválida.[/red]")
        return

    qualidade = "192"

    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    pasta_destino = os.path.join(pasta_projeto, "musicas-baixadas")
    os.makedirs(pasta_destino, exist_ok=True)

    ffmpeg_path = os.path.join(pasta_projeto, "ffmpeg", "ffmpeg.exe")

    console.print("\n[cyan]Iniciando download...[/cyan]\n")

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
        "quiet": False,
        "no_warnings": True,
        "restrictfilenames": False,
    }

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
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()