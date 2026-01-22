# YouTube MP3 Downloader

Conversor simples de YouTube para MP3, feito em Python, criado para substituir serviços online lentos, cheios de anúncios e com restrições artificiais de download.
Utiliza a biblioteca yt-dlp juntamente com um ffmpeg.exe local, dispensando a instalação manual do FFmpeg ou ajustes de variáveis de ambiente.

---

## Tecnologias utilizadas

- **Python 3.x**
- **FFmpeg**
- **yt-dlp**

---

##  Funcionalidades

- Baixa através de uma URL única inserida
- Qualidade fixa em 192 kbps
- Converte automaticamente para **MP3**
- Download direto para a pasta de downloads dentro do projeto
- Interface simples via terminal

---

## Como utilizar o programa

1. Clone o repositório:
   ```bash
   git clone https://github.com/magalhaesmth/youtube-mp3-downloader
    ```

2. Entre na pasta do projeto:

   ```bash
   cd YoutubeMP3Donverter
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Agora é só executar o programa com:

    ```bash
    python main.py
    ```

### Passo a passo:

1. Cole a URL do vídeo do YouTube

2. O MP3 será baixado e salvo automaticamente na pasta `downloads`


## Observações

* O projeto é destinado **apenas para uso pessoal e educativo**
* O nome do arquivo é baseado no título do vídeo