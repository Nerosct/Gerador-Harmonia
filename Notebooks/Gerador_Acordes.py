import customtkinter as ctk
from tkinter import messagebox
from magenta.models.shared import sequence_generator_bundle
from magenta.models.polyphony_rnn import polyphony_sequence_generator, polyphony_model
from magenta.music import sequence_proto_to_midi_file, NoteSequence
from note_seq.protobuf import generator_pb2
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()

# Carregando modelo polyphony_rnn 
BUNDLE_PATH = 'polyphony_rnn.mag'
bundle = sequence_generator_bundle.read_bundle_file(BUNDLE_PATH)

config = polyphony_model.default_configs['polyphony']
config.hparams.batch_size = 64
config.hparams.rnn_layer_sizes = [128, 128]

polyphony_rnn_generator = polyphony_sequence_generator.PolyphonyRnnSequenceGenerator(
    model=polyphony_model.PolyphonyRnnModel(config),
    details=config.details,
    steps_per_quarter=config.steps_per_quarter,
    checkpoint=None,
    bundle=bundle
)
polyphony_rnn_generator.initialize()

# Função de geração 
def gerar_musica():
    try:
        entrada_str = entry_acordes.get().strip()
        tempo_por_acorde = float(entry_tempo.get())
        duracao = float(entry_duracao.get())
        velocidade = int(entry_velocidade.get())
        saida = entry_saida.get().strip()

        if not entrada_str or not saida:
            raise ValueError("Todos os campos devem ser preenchidos.")

        acordes = []
        for grupo in entrada_str.split(';'):
            notas = grupo.strip('() \n').split(',')
            acordes.append([int(n.strip()) for n in notas])

        primer_sequence = NoteSequence()
        primer_sequence.tempos.add(qpm=120)

        for i, acorde in enumerate(acordes):
            for nota in acorde:
                note = primer_sequence.notes.add()
                note.pitch = nota
                note.start_time = i * tempo_por_acorde
                note.end_time = (i + 1) * tempo_por_acorde
                note.velocity = velocidade

        primer_sequence.total_time = len(acordes) * tempo_por_acorde

        generator_options = generator_pb2.GeneratorOptions()
        generate_section = generator_options.generate_sections.add()
        generate_section.start_time = primer_sequence.total_time
        generate_section.end_time = primer_sequence.total_time + duracao

        sequence = polyphony_rnn_generator.generate(primer_sequence, generator_options)
        sequence_proto_to_midi_file(sequence, saida)

        messagebox.showinfo("Sucesso", f"Música polifônica salva em:\n{saida}")
    except Exception as e:
        messagebox.showerror("Erro ao gerar música", str(e))


# === Interface Gráfica ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Gerador Harmônia")
app.geometry("540x560")  # altura aumentada para comportar o botão
app.resizable(False, False)

frame = ctk.CTkFrame(master=app, corner_radius=12)
frame.pack(padx=20, pady=20, fill="both", expand=True)
frame.pack_propagate(False)  # evita que o frame "colapse" e esconda widgets

ctk.CTkLabel(
    master=frame,
    text="🎶 Gerador de Acordes Polifônicos",
    font=("Segoe UI", 20, "bold")
).pack(pady=(20, 10))

campos = [
    ("Acordes (ex: (60,64,67);(62,65,69)):", "(60,64,67);(62,65,69)"),
    ("Tempo por acorde (s):", "0.6"),
    ("Duração da geração (s):", "30"),
    ("Velocidade da nota (0-127):", "80"),
    ("Caminho do arquivo MIDI:", "saida.mid"),
]

entradas = []

for label_text, default in campos:
    ctk.CTkLabel(master=frame, text=label_text, anchor="w", font=("Segoe UI", 12)).pack(padx=20, pady=(10, 0), fill="x")
    entry = ctk.CTkEntry(master=frame, placeholder_text=label_text)
    entry.insert(0, default)
    entry.pack(padx=20, pady=(0, 8), fill="x")
    entradas.append(entry)

entry_acordes, entry_tempo, entry_duracao, entry_velocidade, entry_saida = entradas

# === Botão Gerar Música ===
botao_gerar = ctk.CTkButton(
    master=frame,
    text="🎵 Gerar Música",
    command=gerar_musica,
    corner_radius=10,
    font=("Segoe UI", 13, "bold"),
    width=200,
    height=40,
)
botao_gerar.pack(pady=30)

# Iniciar app
app.mainloop()
