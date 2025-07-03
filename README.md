# Gerador-Harmonia

# Gerador de Acordes Polifônicos com Magenta e CustomTkinter

Este projeto é uma interface gráfica simples para geração de músicas polifônicas (acordes) utilizando o modelo Polyphony RNN da biblioteca [Magenta](https://magenta.tensorflow.org/). O usuário informa uma sequência de acordes, parâmetros de geração e salva o resultado em um arquivo MIDI.

## Funcionalidades
- Interface gráfica moderna com [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Geração de música polifônica baseada em acordes definidos pelo usuário
- Exportação do resultado em formato MIDI
- Personalização de tempo, duração, velocidade das notas e caminho do arquivo de saída

## Pré-requisitos
- Python 3.8.10
- [Magenta](https://github.com/magenta/magenta) (e dependências)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [note-seq](https://github.com/magenta/note-seq)
- TensorFlow 1.x (compatível com Magenta)

Instale as dependências principais com:

```bash
pip install magenta customtkinter note-seq tensorflow==1.15
```

Grupo: Bruna Mafra, Denilson Pereira, Igor Silva, Guilherme Lara, Nathan Marques
