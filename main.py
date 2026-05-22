import subprocess
import os
import wave
from faster_whisper import WhisperModel
from tqdm import tqdm
from halo import Halo
from tkinter import Tk
from tkinter.filedialog import askdirectory
from datetime import datetime









#Declaração de variáveis
diretorio_execucao = os.path.dirname(os.path.abspath(__file__))
# video = os.path.join(diretorio_execucao, "video.mp4")
audio = os.path.join(diretorio_execucao, "audio.wav")









# Declaração de funções
def selecionar_pasta_de_multimidias():

    # Esconde janela principal do tkinter
    root = Tk()
    root.withdraw()

    print("Selecione a pasta com as multimídias")

    pasta = askdirectory(title="Selecione a pasta com as multimídias")

    pasta = os.path.normpath(pasta)
    return pasta


def listar_multimidias(pasta):

    extensoes_multimidia = (
    
    ###VIDEO###
    # formatos modernos comuns
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".webm",
    ".m4v",

    # streaming/web
    ".flv",
    ".f4v",

    # MPEG
    ".mpeg",
    ".mpg",
    ".mp2",
    ".mpe",

    # Windows
    ".wmv",
    ".asf",

    # Apple
    ".qt",

    # mobile/câmeras
    ".3gp",
    ".3g2",

    # Blu-ray/DVD
    ".vob",
    ".mts",
    ".m2ts",
    ".ts",

    # codecs/container modernos
    ".hevc",
    ".h264",
    ".264",

    # formatos menos comuns mas úteis
    ".ogv",
    ".rm",
    ".rmvb",
    ".divx",

    # transporte/stream
    ".mxf",

    # gravações OBS/captura
    ".nut",


    ###AUDIO###
    # formatos modernos/comuns
    ".mp3",
    ".wav",
    ".flac",
    ".aac",
    ".m4a",
    ".opus",
    ".ogg",

    # Windows
    ".wma",

    # Apple
    ".aiff",
    ".aif",
    ".caf",

    # lossless / alta qualidade
    ".alac",
    ".ape",
    ".wv",

    # formatos antigos/comuns
    ".au",
    ".snd",

    # codecs/container variados
    ".ac3",
    ".dts",

    # áudio profissional
    ".pcm",

    # streaming/voz
    ".amr",

    # formatos RealMedia antigos
    ".ra",
    ".ram",

    # MIDI (não é áudio real, mas FFmpeg pode lidar em alguns casos)
    #".mid",
    #".midi",

    # formatos menos comuns
    ".tta",
    ".mka",
    ".oga"
)

    multimidia = []

    for raiz, diretorios, arquivos in os.walk(pasta):

        for arquivo in arquivos:

            if arquivo.lower().endswith(extensoes_multimidia):

                caminho_completo = os.path.normpath(os.path.join(raiz, arquivo))

                multimidia.append(caminho_completo)

    multimidia.sort()

    return multimidia


def carrega_modelo_transcricao():
    spinner = Halo(text="Carregando modelo de transcrição", spinner="dots")
    spinner.start()
    modelo_transcricao = WhisperModel("small", device="cpu", compute_type="int8")
    spinner.succeed("Modelo de transcrição carregado")
    return modelo_transcricao


def converter_para_wav(arquivo_video, arquivo_audio):
    print("Iniciando extração de audio temporário")
    comando = [
        "ffmpeg",
        "-y",               # sobrescreve arquivo de audio se existir
        "-i", arquivo_video,

        "-ar", "16000",     # sample rate
        "-ac", "1",         # mono
        "-loglevel", "error",

        arquivo_audio
    ]

    subprocess.run(comando)
    print("Áudio temporário extraído com sucesso")


def extrair_duracao(arquivo_audio):
    print("Iniciando extração da duração do audio")
    with wave.open(arquivo_audio, "r") as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        duracao = frames / float(rate)

    print(f"Duração do áudio: {duracao:.2f} segundos")
    return duracao


def transcricao(arquivo_audio, duracao_audio, modelo_transcricao):
    text = ""

    print("Carregando áudio para o modelo de transcrição")
    segments, info = modelo_transcricao.transcribe(arquivo_audio, language="pt")
    print("Áudio carregado para o modelo de transcrição")

    if os.path.exists(arquivo_audio):
        os.remove(arquivo_audio)
    print("Arquivo de áudio temporário removido")

    print("Idioma detectado:", info.language)
    print("Probabilidade:", info.language_probability)

    barra_progresso = tqdm(total=duracao_audio, unit="s", desc="Transcrevendo")

    for segment in segments:
        text += segment.text
        novo_valor = min(segment.end, duracao_audio)
        progresso = novo_valor - barra_progresso.n
        barra_progresso.update(progresso)

    barra_progresso.close()
    text = text.strip()

    print("\n--- TRANSCRIÇÃO CONCLUÍDA ---\n")
    
    return text


def salvar_transcricao(arquivo_gravar_transcricao, pasta_multimidia, nome_arquivo_multimidia, texto_transcrito):

    with open(arquivo_gravar_transcricao, "a", encoding="utf-8") as arquivo:

        arquivo.write("\n")
        arquivo.write("=" * 50)
        arquivo.write("\n")

        arquivo.write(f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        arquivo.write(f"ARQUIVO MULTIMÍDIA: {os.path.relpath(nome_arquivo_multimidia, pasta_multimidia)}\n")

        arquivo.write("=" * 50)
        arquivo.write("\n\n")

        arquivo.write(texto_transcrito)

        arquivo.write("\n\n")








#Transcrição
print("Iniciando processo de transcrição\n")

model = carrega_modelo_transcricao()

pasta_de_multimidias = selecionar_pasta_de_multimidias()
multimidias = listar_multimidias(pasta_de_multimidias)
arquivo_transcricao = os.path.join(pasta_de_multimidias, "Transcrição.txt")
if os.path.exists(arquivo_transcricao):
    os.remove(arquivo_transcricao)

for i, arquivo_multimidia in enumerate(multimidias):
    try:
        print("#" * 50)
        print(f"Multimidia {i + 1} de {len(multimidias)}")

        converter_para_wav(arquivo_multimidia, audio)

        duracao_audio = extrair_duracao(audio)

        texto_transcrito = transcricao(audio, duracao_audio, model)

        salvar_transcricao(arquivo_transcricao, pasta_de_multimidias, arquivo_multimidia, texto_transcrito)
        print(f"Texto transcrito salvo em {arquivo_transcricao}")

    except Exception as erro:
        print(f"Erro ao processar {arquivo_multimidia}")
        print(erro)

print ("\nProcesso de transcrição finalizado")






