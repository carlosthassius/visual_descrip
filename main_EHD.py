import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from EHD import EHDDescriptor
import numpy as np
import os

# Variáveis globais
imagem = None
painel_imagem = None
threshold = None

def carregar_imagem():
    '''
    Carrega uma imagem que pode ser usada para obter descritor ou comparar
    '''
    global imagem, painel_imagem

    caminho_imagem = filedialog.askopenfilename()
    
    if caminho_imagem:
        imagem = Image.open(caminho_imagem)
        imagem.thumbnail((300, 300))  # Redimensiona para exibição
        img = ImageTk.PhotoImage(imagem)
        painel_imagem.config(image=img)
        painel_imagem.image = img  # Referência para evitar garbage collection

def interface():
    '''
    Interface do programa
    '''
    global painel_imagem, threshold, root, saida_descritor, entrada_correspondencias
    global frame_resultados, progress_bar, label_progresso

    root = tk.Tk()
    lado, cima = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f'{lado}x{cima}+0+0')
    root.title("Comparador de Imagens com EHD")
    root.configure(bg="black")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", background="#3E64FF", foreground="black",
                    font=("Helvetica", 10, "bold"), padding=6)
    style.configure("TLabel", background="black", foreground="white", font=("Helvetica", 10))
    style.configure("TEntry", padding=5)
    style.configure("TProgressbar", troughcolor="gray25", background="#3E64FF")

    # Frame Principal
    container_esquerdo = tk.Frame(root, bg="black", padx=20, pady=20)
    container_direito = tk.Frame(root, bg="black", padx=20, pady=20)
    container_esquerdo.pack(side="left", fill="y")
    container_direito.pack(side="right", fill="both", expand=True)

    # === LADO ESQUERDO ===
    botoes_container = tk.Frame(container_esquerdo, bg="black")
    botoes_container.pack(pady=5)

    ttk.Button(botoes_container, text="Carregar Imagem", command=carregar_imagem).pack(pady=5)

    painel_imagem = tk.Label(container_esquerdo, bg="black")
    painel_imagem.pack(pady=5)

    ttk.Label(container_esquerdo, text="Limiar:").pack(anchor="w")
    threshold = tk.Entry(container_esquerdo, bg="gray15", fg="white", insertbackground="white")
    threshold.pack(fill="x", pady=5)

    ttk.Label(container_esquerdo, text="Número máximo de correspondências:").pack(anchor="w")
    entrada_correspondencias = tk.Entry(container_esquerdo, bg="gray15", fg="white", insertbackground="white")
    entrada_correspondencias.pack(fill="x", pady=5)

    def obter_descritor():
        try:
            threshold_valor = float(threshold.get())
        except ValueError:
            threshold_valor = 1.0
            print("Limiar inválido. Usando 1.0")

        if imagem:
            descriptor = descriptor_calc(imagem, threshold_valor)
            saida_descritor.config(state='normal')
            saida_descritor.delete(1.0, tk.END)
            saida_descritor.insert(tk.END, "Descritor (resumo):\n")
            saida_descritor.insert(tk.END, ', '.join(f'{x:.2f}' for x in descriptor))
            saida_descritor.config(state='disabled')

    botao_descritor = ttk.Button(container_esquerdo, text="Obter Descritor", command=obter_descritor)
    botao_descritor.pack(pady=5)

    def iniciar_comparacao():
        compare_images(imagem, float(threshold.get()) if threshold.get() else 1.0)
        progress_bar.pack(pady=10)
        label_progresso.pack()

    compare_button = ttk.Button(container_esquerdo, text="Comparar Imagem", command=iniciar_comparacao)
    compare_button.pack(pady=5)

    progress_bar = ttk.Progressbar(container_esquerdo, orient="horizontal", length=200, mode="determinate")
    label_progresso = ttk.Label(container_esquerdo, text="")

    # === LADO DIREITO ===
    ttk.Label(container_direito, text="Descritor extraído:").pack(anchor="w")
    saida_descritor = tk.Text(container_direito, height=10, width=70, wrap=tk.WORD,
                              bg="gray15", fg="white", insertbackground="white")
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

def descriptor_calc(image, threshold_value):
    '''
    Recebe uma imagem e um limiar, aplica a função EHDDescriptor para obter o descritor
    '''
    ehd = EHDDescriptor(threshold=float(threshold_value))
    descriptor = ehd.apply(image)
    return descriptor

def compare_images(image, threshold_value):
    '''
    Realiza efetivamente a comparação entre os descritores das imagens
    '''
    pasta_dataset = "Image_Dataset"
    pasta_descritores = "imagesEHD"
    os.makedirs(pasta_descritores, exist_ok=True)

    for widget in frame_resultados.winfo_children():
        widget.destroy()

    descritor_imagem_principal = descriptor_calc(image, threshold_value)

    try:
        num_correspondencias = int(entrada_correspondencias.get())
    except ValueError:
        num_correspondencias = 5
        print("Valor inválido. Usando 5.")

    resultados_comparacao = []
    arquivos = [f for f in os.listdir(pasta_dataset) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]
    total = len(arquivos)

    progress_bar["maximum"] = total
    progress_bar["value"] = 0

    for i, nome_arquivo in enumerate(arquivos):
        caminho_img = os.path.join(pasta_dataset, nome_arquivo)
        nome_arquivo_ehd = os.path.splitext(nome_arquivo)[0] + ".ehd"
        caminho_ehd = os.path.join(pasta_descritores, nome_arquivo_ehd)

        try:
            if os.path.exists(caminho_ehd):
                descritor_comparar = np.loadtxt(caminho_ehd, delimiter=',')
            else:
                with Image.open(caminho_img) as img:
                    descritor_comparar = descriptor_calc(img, threshold_value)
                    np.savetxt(caminho_ehd, descritor_comparar, delimiter=',')

            distancia = calcular_distancia(descritor_imagem_principal, descritor_comparar)
            resultados_comparacao.append((nome_arquivo, distancia))

        except Exception as e:
            print(f"Erro em {nome_arquivo}: {e}")

        progress_bar["value"] = i + 1
        porcentagem = int((i + 1) / total * 100)
        label_progresso.config(text=f"Progresso: {porcentagem}%")
        root.update_idletasks()

    resultados_comparacao.sort(key=lambda x: x[1])
    top_resultados = resultados_comparacao[:num_correspondencias]

    colunas_maximas = 10
    linha = 0
    coluna = 0

    for nome_arquivo, distancia in top_resultados:
        caminho_img = os.path.join(pasta_dataset, nome_arquivo)
        try:
            img = Image.open(caminho_img)
            img.thumbnail((100, 100))
            img_tk = ImageTk.PhotoImage(img)

            frame_individual = tk.Frame(frame_resultados, bg="black")
            frame_individual.grid(row=linha, column=coluna, padx=10, pady=10)

            label_img = tk.Label(frame_individual, image=img_tk, bg="black")
            label_img.image = img_tk
            label_img.pack()

            label_texto = tk.Label(frame_individual, text=f"{nome_arquivo[:20]}\nDistância: {distancia:.2f}", fg="white", bg="black")
            label_texto.pack()

            coluna += 1
            if coluna >= colunas_maximas:
                coluna = 0
                linha += 1
        except Exception as e:
            print(f"Erro ao exibir {nome_arquivo}: {e}")

def calcular_distancia(descritor1, descritor2):
    '''
    Calcula a distância euclidiana entre descritores
    '''
    descritor1 = np.array(descritor1)
    descritor2 = np.array(descritor2)
    return np.linalg.norm(descritor1 - descritor2)

try:
    interface()
except:
    print("Ocorreu um erro ao abrir a interface")

'''
FALTA FAZER

Tratamento de erros
Validação de dados (tipo está correto? e se pedir mais correspondências do que tem no dataset?)

'''
