# si considerano filtri puntuali tutti quelli che nella forula che modificano il pixel
# appare solo sulla base della propria posizione e del proprio valore
# NON SI USANO FILTRI DI CONVOLUZIONE

import cv2
import numpy as np
import matplotlib.pyplot as plt # usata per mostrare grafici ed immagini



# funzione di appoggio per overflow detection
def _overflow_detection(result):
    overflow_detected = np.isinf(result)
    
    # Stampa un messaggio se è stato rilevato un overflow
    if np.any(overflow_detected):
        print("Overflow oltre i limiti di float32 rilevato in alcuni pixel!")

    return True



# 5. Clamping (riduzione del range)
def clamping(img, a, b):
    # clippa i valori minori di 'a' ad un valore 'a' e quelli maggiori di 'b' al valore di 'b'
    result = np.clip(img, a, b)
    return result.astype(np.uint8)



# 4. Operatore Lineare (addizione + moltiplicazione)
def linear_operator(img, k, c):
    result = img.astype(np.float32) * k + c # aumento rappresentabilità per evitare overflow
    _overflow_detection(result)
    return clamping(img, 0, 255)


# 1. Saturated Arithmetic
def saturated_arithmetic(img, c):
    result = linear_operator(img, 1, c)
    return result



# 3. Moltiplicazione (uguale ma moltipilca)
def multiply_brightness(img, k):
    result = linear_operator(img, k, 0)
    return result






# 6. Inversione dei livelli di grigio
def gray_level_inversion(img):
    # Livello massimo per immagini 8-bit
    L = 255  
    # rende l' intera immagine col valore opposto
    # (ogni pixel ha un valore speculare alla metà del valore massimo (127,5) )
    result = L - img
    return result




#UTILIZZO DEL ISTOGRAMMA (sono sempre puntuali)

#7. Constrast Stretching
def constrast_stretching(img, new_min=0, new_max=255):
    min_val, max_val = np.min(img), np.max(img)
    return ((img - min_val) / (max_val - min_val) * ((new_max-new_min)+new_min)).astype(np.uint8) # meglio forzare il tipo ad intero


#8. Equalizzazione dell'Istogramma
def histogram_equalization(img):
    # appiattisce l'istogramma per immagini bianco e nero
    return cv2.equalizeHist(img)

# 9. CLAHE (Contrast Limited Adaptive Histogram Equalization) [tenta di evitare sovra-illuminazione e sovra-oscuramento]
    # suddivide l'immagine in blocchi (tiles)
    # applica l'equazione del istogramma solo localmente
    # imposta liminte di contrasto per ogni zona
    # usa l'interpolazione per evitare una chiara divisione tra i tiles [i pixel di confine sono una media di valori dei pixel dei blocchi]
def clahe(img, clip_limit=2.0, tile_grid_size=(8, 8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(img)

# 10. Thresholding [di solito usato per dividere sfondo e soggetto]
    # thresh_value -> pixel con valori inferire diventano nero (0) altrimenti diventano bianco (1)
def thresholding(img, thresh_value):
    # cv2.THRESH_BINARY -> specifica che si vuole la binarizzazione bianco/nero
    _, result = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)
    return result

# 11. Otsu’s Binarization [versione automatizzata ed algoritmica di thresholding (non dobbiamo scegliere noi il valore migliore)]
def otsu_binarization(img):
    _, result = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return result

# 12. Adaptive Thresholding [fa diversi valori di soglia a seconda della zona dell'immagine]
def adaptive_thresholding(img, block_size=3, C=2):
    '''
    Arg
        block_size: dimensioni blocco
        C: Soglia=media dei valori dei pixel nel blocco−C
    '''
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)

# 13. Linear Blending [mescola due immagini]
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
