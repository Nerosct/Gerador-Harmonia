import customtkinter as ctk
from tkinter import messagebox
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from magenta.music import sequence_proto_to_midi_file, NoteSequence, note_seq
from note_seq.protobuf import generator_pb2
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# Inicializar modelo
BUNDLE_PATH = 'basic_rnn.mag'
bundle = sequence_generator_bundle.read_bundle_file(BUNDLE_PATH)
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()

# Configurações da interface
ctk.set_appearance_mode("dark")  # opções: "light", "dark", "system"
ctk.set_default_color_theme("green")  # opções: blue, green, dark-blue

# Função de geração de melodia
def gerar_melodia():
    try:
        notas_str = entry_notas.get()
        notas = [int(n) for n in notas_str.split(',')]
        tempo_por_nota = float(entry_tempo.get())
        duracao = float(entry_duracao.get())
        velocidade = int(entry_velocidade.get())
        saida = entry_saida.get()

        primer_sequence = NoteSequence()
        primer_sequence.tempos.add(qpm=120)

        for i, nota in enumerate(notas):
            note = primer_sequence.notes.add()
            note.pitch = nota
            note.start_time = i * tempo_por_nota
            note.end_time = (i + 1) * tempo_por_nota
            note.velocity = velocidade
        primer_sequence.total_time = len(notas) * tempo_por_nota

        generator_options = generator_pb2.GeneratorOptions()
        generate_section = generator_options.generate_sections.add()
        generate_section.start_time = primer_sequence.total_time
        generate_section.end_time = primer_sequence.total_time + duracao

        sequence = melody_rnn.generate(primer_sequence, generator_options)
        sequence_proto_to_midi_file(sequence, saida)
        messagebox.showinfo("Sucesso", f"Melodia salva como {saida}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Janela principal
app = ctk.CTk()
app.title("Gerador de Melodias")
app.geometry("600x550")

# Título
titulo = ctk.CTkLabel(app, text="Gerador de Melodias", font=ctk.CTkFont(size=18, weight="bold"))
titulo.pack(pady=20)

# Frame dos campos
frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=10, fill="both", expand=True)

# Lista de campos
entradas = {}

def adicionar_entrada(nome, padrão, row):
    label = ctk.CTkLabel(frame, text=nome)
    label.grid(row=row, column=0, padx=10, pady=8, sticky="e")
    entry = ctk.CTkEntry(frame, width=250)
    entry.insert(0, padrão)
    entry.grid(row=row, column=1, padx=10, pady=8)
    entradas[nome] = entry

adicionar_entrada("Notas iniciais (ex: 60,64,67):", "60,64,67", 0)
adicionar_entrada("Tempo por nota (s):", "0.5", 1)
adicionar_entrada("Duração da geração (s):", "20", 2)
adicionar_entrada("Velocidade da nota (0-127):", "40", 3)
adicionar_entrada("Caminho do arquivo MIDI:", "../midis/melodia.mid", 4)

entry_notas = entradas["Notas iniciais (ex: 60,64,67):"]
entry_tempo = entradas["Tempo por nota (s):"]
entry_duracao = entradas["Duração da geração (s):"]
entry_velocidade = entradas["Velocidade da nota (0-127):"]
entry_saida = entradas["Caminho do arquivo MIDI:"]

# Botão
botao = ctk.CTkButton(app, text="🎼 Gerar Melodia", command=gerar_melodia, width=200)
botao.pack(pady=20)

# Executar interface
app.mainloop()
