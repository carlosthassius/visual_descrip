from PIL import Image
from EHD import EHDDescriptor
import matplotlib.pyplot as plt
import numpy as np

img = Image.open('img1.jpg')
ehd = EHDDescriptor(threshold=50)
histograma = ehd.apply(img)
histograma_quantizado = ehd.quantize(histograma)

print(histograma_quantizado)

plt.figure(figsize=(14, 5))
plt.bar(np.arange(len(histograma_quantizado)), histograma_quantizado, color='skyblue')
plt.title("Histograma Quantizado do Descritor EHD")
plt.xlabel("Índice do Bin")
plt.ylabel("Frequência")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()