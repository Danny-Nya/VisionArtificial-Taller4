import cv2
import numpy as np
import matplotlib.pyplot as plt

def connected_component_label():
    #Leer imagen
    path = "Figures2.jpg"
    img = cv2.imread(path, 0)
    # Converitir a nibario
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    #Aplicar connectedComponents
    num_labels, labels = cv2.connectedComponents(img)
    # crear una tabla de zeros para ingresar los tamanos de regiones
    regions = np.zeros(num_labels)
    #alto y ancho de la imagen
    height = img.shape[0]
    width = img.shape[1]
    #buscar los elementos con el mismo marcador asi tener la cantidad de pixeles
    for lab in range(num_labels):
        for x in range(height):
            for y in range(width):
                if labels[x, y] == lab:
                    regions[lab] = regions[lab] + 1
    #eliminar la region de maracores de negro
    regions[0] = 0
    #calcular el 15% de la region mas grande
    minsize = max(regions) * 0.15


    print("Numero de Regiones:"+str(num_labels))
    i=1
    for region in regions:
        print("Region "+str(i)+": "+str(region)+" pixeles")
        i+=1
    num_labels_final=num_labels
    for lab in range(num_labels):
        if regions[lab] < minsize:
            regions[lab] = 0
            num_labels_final-=1
            for x in range(height):
                for y in range(width):
                    if labels[x, y] == lab:
                        labels[x, y] = 0
                        img[x, y] = 0
    i=1
    print("_________________________________________________")
    print("Numero de Regiones Finales:" + str(num_labels_final))
    for region in regions:
        if region!=0:
            print("Region "+str(i)+": "+str(region)+" pixeles")
            i += 1

    # Reango de colores
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # convertir a BGR
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # Defnir el fondo negro
    labeled_img[label_hue == 0] = 0

    # Guardar imagen Binaria
    cv2.imwrite('Binaria.png',cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


    # Guardar imagen Con colores
    cv2.imwrite('Segmentada_Colores.png',labeled_img)
    #Erosionar las regiones
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.erode(img, kernel)

    cv2.imwrite('Erosionada.png',img)

    #Transformada de distancia
    dist_transform = cv2.distanceTransform(img, cv2.DIST_L2, 5)
    #zonas seguras
    ret, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)

    cv2.imwrite('TransformadaDistancia.png', dist_transform)
    cv2.imwrite('SegmentosSeguros.png', sure_fg)

    #binarizar la imagen resultante
    sure_fg = cv2.threshold(sure_fg, 127, 255, cv2.THRESH_BINARY)[1]
    sure_fg=np.uint8(sure_fg)
    #rehacer marcadores
    num_labels2, labels2 = cv2.connectedComponents(sure_fg)
    lab=1
    #encontrar las cordenadas de las regiones
    print("_________________________________________________")
    print("Coordenadas:")
    for x in range(height):
        for y in range(width):
            if labels2[x, y] ==lab and labels2[x, y] !=0:
                print("Coordenadas region "+str(lab)+": "+str([x,y]))
                lab+=1

def main():
    connected_component_label()


if __name__ == "__main__":
    main()
