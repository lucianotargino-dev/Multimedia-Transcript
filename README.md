# Multimedia Transcript

Transcrição automática em lote de arquivos de áudio e vídeo utilizando Faster-Whisper.

O projeto permite selecionar uma pasta contendo mídias, processar automaticamente todos os arquivos compatíveis e gerar um único arquivo `.txt` com as transcrições organizadas.

Ideal para:

- Transcrição de podcasts
- Aulas
- Entrevistas
- Reuniões
- Arquivos pessoais
- Grandes e pequenos volumes de mídia

---

# Funcionalidades

- Transcrição automática em lote
- Suporte a dezenas de formatos de áudio e vídeo
- Extração automática de áudio via FFmpeg
- Barra de progresso
- Indicador visual de processamento
- Organização automática das transcrições
- Geração de arquivo `.txt`
- Interface simples para seleção de pasta
- Compatível com modelos Whisper locais

---

# Tecnologias utilizadas

- Python
- Faster-Whisper
- FFmpeg
- Tkinter
- TQDM
- Halo

---

# Requisitos

- Python 3.10+
- FFmpeg instalado e disponível no PATH do sistema

## Instalação do FFmpeg

### Windows

Baixe em:
[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Depois adicione o FFmpeg ao PATH do Windows.

### Linux

```bash
sudo apt install ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

---

# Instalação do projeto

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/multimedia-transcript.git
```

Entre na pasta:

```bash
cd multimedia-transcript
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

# Como usar

Execute o projeto:

```bash
python main.py
```

Ao iniciar:

1. Uma janela será aberta
2. Selecione a pasta contendo os arquivos multimídia
3. O processamento começará automaticamente
4. Ao final, será gerado um arquivo `Transcrição.txt`, na mesma pasta escolhida inicialmente com os arquivos multimídia, com todas as transcrições organizadas.

---

# Modelos Whisper

O projeto utiliza Faster-Whisper e permite alterar facilmente o modelo utilizado.

Exemplo atual:

```python
model = WhisperModel("small")
```

## Modelos disponíveis

| Modelo   | Velocidade   | Qualidade | Uso de RAM/VRAM |
| -------- | ------------ | --------- | --------------- |
| tiny     | Muito rápida | Baixa     | Muito baixo     |
| base     | Rápida       | Básica    | Baixo           |
| small    | Boa          | Boa       | Médio           |
| medium   | Mais lenta   | Muito boa | Alto            |
| large-v3 | Lenta        | Excelente | Muito alto      |

## Como alterar

Basta modificar:

```python
WhisperModel("small")
```

Para:

```python
WhisperModel("medium")
```

Por exemplo.

> O modelo `small` foi utilizado durante os testes do projeto por oferecer um bom equilíbrio entre velocidade, consumo de memória e qualidade de transcrição em máquinas mais simples.

---

# Aceleração por GPU (CUDA)

O Faster-Whisper suporta aceleração por GPU utilizando CUDA, o que pode aumentar drasticamente a velocidade das transcrições.

## Exemplo usando GPU NVIDIA

```python
modelo_transcricao = WhisperModel("small", device="cuda", compute_type="float16")
```

## Exemplo usando apenas CPU

```python
modelo_transcricao = WhisperModel("small", device="cpu", compute_type="int8")
```

---

# Modos recomendados

| Hardware   | Configuração recomendada    |
| ---------- | --------------------------- |
| CPU fraca  | `device="cpu"` + `int8`     |
| CPU forte  | `device="cpu"` + `float32`  |
| GPU NVIDIA | `device="cuda"` + `float16` |

---

# Observações sobre CUDA

- Requer GPU NVIDIA compatível
- Requer instalação do CUDA Toolkit
- Recomendado para grandes volumes de mídia
- Modelos maiores se beneficiam muito da GPU

---

# Exemplo completo

```python
modelo_transcricao = WhisperModel("small", device="cuda", compute_type="float16")
```

---

# Formatos suportados

### Vídeo

```
.mp4 .mkv .mov .avi .webm .m4v
.flv .f4v
.mpeg .mpg .mp2 .mpe
.wmv .asf
.qt
.3gp .3g2
.vob .mts .m2ts .ts
.hevc .h264 .264
.ogv .rm .rmvb .divx
.mxf
.nut
```

### Áudio

```
.mp3 .wav .flac .aac .m4a .opus .ogg
.wma
.aiff .aif .caf
.alac .ape .wv
.au .snd
.ac3 .dts
.pcm
.amr
.ra .ram
.tta .mka .oga
```

---

# Estrutura do projeto

```
multimedia-transcript/
│
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
```

---

# Arquivos gerados

Durante o processamento podem ser gerados:

| Arquivo         | Descrição                                       |
| --------------- | ----------------------------------------------- |
| Transcrição.txt | Resultado final das transcrições                |
| audio.wav       | Arquivo temporário utilizado durante a extração |

---

# Observações

- O primeiro uso pode demorar devido ao download automático do modelo Whisper.
- Modelos maiores exigem mais RAM/VRAM.
- O desempenho depende bastante do hardware utilizado.
- O processamento ocorre localmente na máquina do usuário.

---

# Exemplo de uso real

O projeto já foi utilizado para processar:

- 89 arquivos multimídia
- Mais de 8 GB de mídia
- Transcrição contínua durante várias horas

---

# Licença

Este projeto está licenciado sob a licença MIT.

Você pode utilizar, modificar e distribuir livremente o código, respeitando os termos da licença.

Para mais detalhes, consulte o arquivo `LICENSE`.
