
# 📷 visual_descrip

Aplicação desenvolvida em Python para extração e uso de descritores visuais MPEG-7, especificamente o **Edge Histogram Descriptor (EHD)**, com o objetivo de identificar as imagens mais semelhantes a uma imagem de consulta (*query image*) em um conjunto de imagens.

---

## 🎯 Objetivo

O projeto permite:

- Calcular o descritor EHD de uma imagem com base no padrão MPEG-7.
- Comparar o descritor da imagem de entrada com os de outras imagens em um diretório.
- Identificar e exibir as imagens mais semelhantes, com base na **distância euclidiana** entre os vetores de descritores.

---

## 🧩 Estrutura do Projeto

- `ehd.py`: Implementação do descritor **Edge Histogram Descriptor (EHD)** com quantização, normalização e extração conforme o padrão MPEG-7.
- `matcher.py`: Responsável por comparar o descritor da imagem de entrada com os descritores de um dataset, utilizando distância euclidiana.
- `interface.py`: Interface gráfica feita com **Tkinter**, que permite carregar imagens, configurar parâmetros e visualizar os resultados da comparação.

---

## 🖥️ Interface Gráfica

A interface permite:

- Carregar uma imagem de consulta.
- Definir o **limiar de borda (threshold)** e o número de imagens semelhantes a serem retornadas.
- Exibir o vetor do descritor extraído.
- Iniciar a comparação com o diretório de imagens.
- Visualizar os resultados com miniaturas e distâncias calculadas.
- Acompanhar o progresso por uma barra de carregamento.

---

## 🛠️ Requisitos

- Python 3.x

### Bibliotecas necessárias:

- `numpy`
- `Pillow`
- `tkinter` (incluso por padrão no Python)
- `os`

Instale os requisitos com:

```bash
pip install numpy pillow
```

---

## 🚀 Como Executar

Clone o repositório:

```bash
git clone https://github.com/carlosthassius/visual_descrip.git
cd visual_descrip
```

Execute a interface:

```bash
python interface.py
```

Use a interface para:

- Carregar a imagem de consulta.
- Definir limiar e número de resultados desejados.
- Visualizar imagens semelhantes do dataset.

---

## 🗂️ Organização de Diretórios

- Certifique-se de que as imagens do dataset estejam em uma pasta local especificada no código (por padrão: `Image_Dataset/`).
- Os descritores das imagens do dataset são **pré-processados** na primeira execução para acelerar comparações futuras.

---

## 🧪 Exemplo de Uso

1. Carregue a imagem principal.
2. Ajuste o limiar ou mantenha o padrão (`50`).
3. Clique em **"Comparar"**.
4. Veja os resultados ordenados por similaridade.

---

## 📌 Observações

- O algoritmo segue o padrão **MPEG-7** para o descritor EHD, com **5 direções** e **16 blocos**, totalizando **80 bins**.
- O cálculo é feito sobre a imagem convertida para tons de cinza com base na **luminância perceptual**.
- Os descritores são quantizados em **8 níveis**, conforme a tabela padrão MPEG-7.

---

## 📈 Melhorias Futuras

- Suporte a outros descritores (ex: de cor, forma).
- Suporte a comparação com múltiplos diretórios.
- Otimização do tempo de carregamento e comparação.
- Versão web com interface responsiva.

---

## 📄 Licença

Este projeto é **acadêmico** e foi desenvolvido no contexto da disciplina **Processamento Audiovisual** no Departamento de Engenharia Eletrotécnica e de Computadores - **Universidade de Coimbra**.