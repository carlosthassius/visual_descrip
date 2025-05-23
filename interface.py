import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
from matcher import descriptor_calc, compare_images

# Variáveis globais
imagem = None
painel_imagem = None
threshold = None
root = None
saida_descritor = None
entrada_correspondencias = None
frame_resultados = None
progress_bar = None
label_progresso = None

def load_image():
    global imagem, painel_imagem

    caminho_imagem = filedialog.askopenfilename()
    if caminho_imagem:
        imagem = Image.open(caminho_imagem)
        imagem.thumbnail((300, 300))
        img = ImageTk.PhotoImage(imagem)
        painel_imagem.config(image=img)
        painel_imagem.image = img

def get_descriptor():
    try:
        threshold_valor = float(threshold.get())
    except ValueError:
        threshold_valor = 50.0

    if imagem:
        descriptor = descriptor_calc(imagem, threshold_valor)
        saida_descritor.config(state='normal')
        saida_descritor.delete(1.0, tk.END)
        saida_descritor.insert(tk.END, ', '.join(f'{x:.2f}' for x in descriptor))
        saida_descritor.config(state='disabled')

def init_comparison():
    try:
        limiar = float(threshold.get())
    except ValueError:
        limiar = 50.0
    try:
        num_resultados = int(entrada_correspondencias.get())
    except ValueError:
        num_resultados = 5

    progress_bar.pack(pady=10)
    label_progresso.pack()
    resultados = compare_images(imagem, limiar, num_resultados, progress_bar, label_progresso, root)
    show_results(resultados, frame_resultados)

def show_results(resultados, frame_destino):
    """
    Mostra os resultados no frame da interface.
    """
    for widget in frame_destino.winfo_children():
        widget.destroy()

    for nome_arquivo, distancia in resultados:
        caminho_imagem = os.path.join("Image_Dataset", nome_arquivo)

        try:
            imagem = Image.open(caminho_imagem)
            imagem.thumbnail((100, 100))
            img_tk = ImageTk.PhotoImage(imagem)

            container = ttk.Frame(frame_destino, padding=10)
            container.pack(fill="x", pady=5)

            label_img = ttk.Label(container, image=img_tk)
            label_img.image = img_tk  # Evita garbage collection
            label_img.pack(side="left")

            info = f"{nome_arquivo}\nDistância: {distancia:.2f}"
            ttk.Label(container, text=info, font=("Helvetica", 10)).pack(side="left", padx=10)

        except Exception as e:
            print(f"Erro ao carregar imagem {nome_arquivo}: {e}")

def interface():
    global painel_imagem, threshold, root, saida_descritor, entrada_correspondencias
    global frame_resultados, progress_bar, label_progresso

    root = tk.Tk()
    lado, cima = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f'{lado}x{cima}+0+0')
    root.title("Comparador de Imagens com EHD")
    root.configure(bg="black")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", background="#3E64FF", foreground="black", font=("Helvetica", 10, "bold"), padding=6)
    style.configure("TLabel", background="black", foreground="white", font=("Helvetica", 10))
    style.configure("TEntry", padding=5)
    style.configure("TProgressbar", troughcolor="gray25", background="#3E64FF")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir, "aguia_icon.png")
    if os.path.exists(icon_path):
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        root.iconphoto(True, icon_photo)

    container_esquerdo = tk.Frame(root, bg="black", padx=20, pady=20)
    container_direito = tk.Frame(root, bg="black", padx=20, pady=20)
    container_esquerdo.pack(side="left", fill="y")
    container_direito.pack(side="right", fill="both", expand=True)

    # Lado esquerdo
    botoes_container = tk.Frame(container_esquerdo, bg="black")
    botoes_container.pack(pady=5)

    ttk.Button(botoes_container, text="Carregar Imagem", command=load_image).pack(pady=5)

    painel_imagem = tk.Label(container_esquerdo, bg="black")
    painel_imagem.pack(pady=5)

    ttk.Label(container_esquerdo, text="Limiar (padrão: 50)").pack(anchor="w")
    threshold = tk.Entry(container_esquerdo, bg="gray15", fg="white", insertbackground="white")
    threshold.pack(fill="x", pady=5)

    ttk.Label(container_esquerdo, text="Correspondências (padrão: 5)").pack(anchor="w")
    entrada_correspondencias = tk.Entry(container_esquerdo, bg="gray15", fg="white", insertbackground="white")
    entrada_correspondencias.pack(fill="x", pady=5)

    ttk.Button(container_esquerdo, text="Obter Descritor", command=get_descriptor).pack(pady=5)
    ttk.Button(container_esquerdo, text="Comparar Imagem", command=init_comparison).pack(pady=5)

    progress_bar = ttk.Progressbar(container_esquerdo, orient="horizontal", length=200, mode="determinate")
    label_progresso = ttk.Label(container_esquerdo, text="")

    # Lado direito
    ttk.Label(container_direito, text="Descritor extraído:").pack(anchor="w")
    saida_descritor = tk.Text(container_direito, height=10, width=70, wrap=tk.WORD,
                              bg="gray15", fg="white", insertbackground="white")
    saida_descritor.configure(font=("Helvetica", 14))
    saida_descritor.pack(fill="x", pady=10)
    saida_descritor.config(state='disabled')
    
    canvas_resultados = tk.Canvas(container_direito, bg="black", height=400)
    scrollbar_vertical = ttk.Scrollbar(container_direito, orient="vertical", command=canvas_resultados.yview)
    canvas_resultados.configure(yscrollcommand=scrollbar_vertical.set)

    scrollbar_vertical.pack(side="right", fill="y")
    canvas_resultados.pack(side="left", fill="both", expand=True)

    frame_resultados = tk.Frame(canvas_resultados, bg="black")
    canvas_resultados.create_window((0, 0), window=frame_resultados, anchor="nw")

    def on_frame_configure(event):
        canvas_resultados.configure(scrollregion=canvas_resultados.bbox("all"))

    frame_resultados.bind("<Configure>", on_frame_configure)

    root.mainloop()

if __name__ == "__main__":
    try:
        interface()
    except Exception as e:
        print("Erro ao iniciar a interface:", e)
