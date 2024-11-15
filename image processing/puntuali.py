# si considerano filtri puntuali tutti quelli che nella forula che modificano il pixel
# appare solo sulla base della propria posizione e del proprio valore
# NON SI USANO FILTRI DI CONVOLUZIONE

import cv2
import numpy as np
import matplotlib.pyplot as plt # usata per mostrare grafici ed immagini


# Carica l'immagine (convertita in scala di grigi)
    # Lenna.png -> percorso dell'immagine
        # cv2.IMREAD_COLOR -> immagine a colori
        # cv2.IMREAD_GRAYSCALE -> immagine in scala di grigi
def read_grayscale(name):
    return cv2.imread(name, cv2.IMREAD_GRAYSCALE)

# Funzione per mostrare le immagini in bianco e nero
def show_image(title, img):
        # cmap= gray rappresenta in scala di grigi
    plt.imshow(img, cmap="gray")
    plt.title(title)
    plt.axis("off")
    plt.show()




# 1. Saturated Arithmetic
def saturated_arithmetic(img, c):
    # somma un valore c a ogni pixel sensa però andare oltre i valoti consentiti
    result = np.clip(img + c, 0, 255)
    # conversione del immagine in 8 bit (quindi con range da 0 - 255)
    return result.astype(np.uint8)

# 3. Moltiplicazione (uguale ma moltipilca)
def multiply_brightness(img, k):
    result = img * k
    return np.clip(result, 0, 255).astype(np.uint8)

# 4. Operatore Lineare (addizione + moltiplicazione)
def linear_operator(img, k, c):
    result = img * k + c
    return np.clip(result, 0, 255).astype(np.uint8)

# 5. Clamping (riduzione del range)
def clamping(img, a, b):
    # clippa i valori minori di 'a' ad un valore 'a' e quelli maggiori di 'b' al valore di 'b'
    result = np.clip(img, a, b)
    return result.astype(np.uint8)

# 6. Inversione dei livelli di grigio
def gray_level_inversion(img):
    # Livello massimo per immagini 8-bit
    L = 255  
    # rende l' intera immagine col valore opposto
    # (ogni pixel ha un valore speculare alla metà del valore massimo (127,5) )
    result = L - img
    return result




#UTILIZZO DEL ISTOGRAMMA (sono sempre puntuali)


# 7. Equalizzazione dell'Istogramma
def histogram_equalization(img):
    # appiattisce l'istogramma per immagini bianco e nero
    return cv2.equalizeHist(img)

# 8. CLAHE (Contrast Limited Adaptive Histogram Equalization) [tenta di evitare sovra-illuminazione e sovra-oscuramento]
    # suddivide l'immagine in blocchi (tiles)
    # applica l'equazione del istogramma solo localmente
    # imposta liminte di contrasto per ogni zona
    # usa l'interpolazione per evitare una chiara divisione tra i tiles [i pixel di confine sono una media di valori dei pixel dei blocchi]
def clahe(img, clip_limit=2.0, tile_grid_size=(8, 8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(img)

# 9. Thresholding [di solito usato per dividere sfondo e soggetto]
    # thresh_value -> pixel con valori inferire diventano nero (0) altrimenti diventano bianco (1)
def thresholding(img, thresh_value):
    # cv2.THRESH_BINARY -> specifica che si vuole la binarizzazione bianco/nero
    _, result = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)
    return result

# 10. Otsu’s Binarization [versione automatizzata ed algoritmica di thresholding (non dobbiamo scegliere noi il valore migliore)]
def otsu_binarization(img):
    _, result = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return result

# 11. Adaptive Thresholding [fa diversi valori di soglia a seconda della zona dell'immagine]
def adaptive_thresholding(img, block_size=11, C=2):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)

# 12. Linear Blending [mescola due immagini]
def linear_blending(img1, img2, alpha=0.5):
    return cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)

# Esempi di applicazione
#show_image("Original Image", image)

#show_image("Saturated Arithmetic", saturated_arithmetic(image, 50))
#show_image("Add Brightness", add_brightness(image, 50))
#show_image("Multiply Brightness", multiply_brightness(image, 1.5))
#show_image("Linear Operator", linear_operator(image, 1.5, -20))
#show_image("Clamping", clamping(image, 50, 200))
#show_image("Gray Level Inversion", gray_level_inversion(image))
#show_image("Histogram Equalization", histogram_equalization(image))
#show_image("CLAHE", clahe(image))
#show_image("Thresholding", thresholding(image, 127))
#show_image("Otsu's Binarization", otsu_binarization(image))
#show_image("Adaptive Thresholding", adaptive_thresholding(image))

# Per linear blending, si consiglia di caricare una seconda immagine per fusione
# image2 = cv2.imread("second_image.jpg", cv2.IMREAD_GRAYSCALE)
# show_image("Linear Blending", linear_blending(image, image2, 0.5))
