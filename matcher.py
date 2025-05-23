import os
import numpy as np
from PIL import Image
from EHD import EHDDescriptor

def descriptor_calc(image, threshold_value):
    """
    Aplica o EHDDescriptor à imagem fornecida com o limiar especificado.
    """
    ehd = EHDDescriptor(threshold=float(threshold_value))
    return ehd.apply(image)

def get_distance(descritor1, descritor2):
    """
    Calcula a distância euclidiana entre dois vetores de descritores.
    """
    descritor1 = np.array(descritor1)
    descritor2 = np.array(descritor2)
    return np.linalg.norm(descritor1 - descritor2)

def compare_images(imagem_principal, threshold_value, max_resultados, progress_bar, label_progresso, root):
    """
    Compara a imagem principal com as imagens do diretório 'dataset',
    retornando as mais semelhantes com base no EHD.
    """
    if imagem_principal is None:
        return []

    dataset_dir = "Image_Dataset"
    descritores_dir = "descriptors"
    os.makedirs(descritores_dir, exist_ok=True)

    descritor_principal = descriptor_calc(imagem_principal, threshold_value)
    resultados = []
    
    arquivos = [f for f in os.listdir(dataset_dir)
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]

    total = len(arquivos)
    for i, nome_arquivo in enumerate(arquivos):
        caminho_img = os.path.join(dataset_dir, nome_arquivo)
        caminho_descritor = os.path.join(descritores_dir, os.path.splitext(nome_arquivo)[0] + ".ehd")

        try:
            if os.path.exists(caminho_descritor):
                descritor = np.loadtxt(caminho_descritor, delimiter=",")
            else:
                with Image.open(caminho_img) as img:
                    descritor = descriptor_calc(img, threshold_value)
                    np.savetxt(caminho_descritor, descritor, delimiter=",")

            distancia = get_distance(descritor_principal, descritor)
            resultados.append((nome_arquivo, distancia))

        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")

        progresso = int((i + 1) / total * 100)
        progress_bar["value"] = progresso
        label_progresso.config(text=f"{progresso}%")
        root.update_idletasks()

    resultados_ordenados = sorted(resultados, key=lambda x: x[1])
    return resultados_ordenados[:max_resultados]
