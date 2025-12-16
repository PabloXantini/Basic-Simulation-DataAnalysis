import math
from scipy.stats import t
import numpy as np

class validacion:
    def __init__(self):
        print("Buenas")

    def main(self):
        #validacion.caso1()
        #validacion.caso2()
        #validacion.caso3()
        #validacion.caso4()
        validacion.caso5()
        #validacion.caso8()
    def caso1(self):
        print("Caso 1. Determinar si el simulador es representativo si la muestra de 100 datos tiene una media de 340 piezas, con un promedio real de 365 piezas y desviación de 21. a = 4%")
        promr = 340
        media = 365
        desvi = 21
        n = 100
        a = 0.04

        Zobs = (media - promr)/(desvi/math.sqrt(n))
        print("Nos da que la observada es", Zobs)

        tcrit = t.ppf(a/2, df=np.inf)
        print("Nos da que la esperada es", tcrit)

        if(Zobs < tcrit):
            print("\nComo la observada", Zobs, "es menor que la esperada", tcrit, "entonces se acepta la representatividad del programa")
        else:
            print("\nComo la observada", Zobs, "es mayor que la esperada", tcrit, "entonces se rechaza la representatividad del programa")

    def caso2(self):
        print("Caso 2. Determinar si el simulador es representativo si tenemos 2 muestras de 175 y 134 más una media de 70 y 73 respectivamente, con una desviación de 11.2. a = 3%")
        x1 = 70
        x2 = 73
        n1 = 175
        n2 = 134
        desvi = 11.2
        a = 0.03

        Zobs = (x1 - x2)/((desvi/n1)+(desvi/n2))
        print("Nos da que la observada es", Zobs)

        tcrit = t.ppf(a/2, df=np.inf)
        print("Nos da que la esperada es", tcrit)

        if(Zobs < tcrit):
            print("\nComo la observada", Zobs, "es menor que la esperada", tcrit, "entonces se acepta la representatividad del programa")
        else:
            print("\nComo la observada", Zobs, "es mayor que la esperada", tcrit, "entonces se rechaza la representatividad del programa")

    def caso3(self):
        print("Caso 3. Un restaurante vende un promedio de 123 ceviches con una desviación de 23, si nuestra muestra es de 120 datos y tenemos un promedio real de 120 determinar, en caso de que si se comporta normal. a = 10%")
        promr = 123
        media = 120
        desvi = 23
        n = 120
        a = 0.1

        Zobs = (media - promr)/(desvi/math.sqrt(n))
        print("Nos da que la observada es", Zobs)

        tcrit = t.ppf(a/2, df=np.inf)
        print("Nos da que la esperada es", tcrit)

        if(Zobs < tcrit):
            print("\nComo la observada", Zobs, "es menor que la esperada", tcrit, "entonces se acepta la representatividad del programa")
        else:
            print("\nComo la observada", Zobs, "es mayor que la esperada", tcrit, "entonces se rechaza la representatividad del programa")

    def caso4(self):
        print("Caso 4. Tenemos 2 muestras simuladas mayores a 30, dándonos N1 = 80 y N2 = 120, con idénticas varianzas x1 = 75.4, s^2 = 6.5, x2 = 115.3, s^2 = 6.5. Calcular el estadístico observado. a = 2%")
        median1 = 75.4
        median2 = 115.3
        s2s =6.5
        s2r = 6.5
        a = 0.02
        n1 = 80
        n2 = 120

        Zobs = (median1 - median2)/((s2s/n1)+(s2r/n2))
        print("Nos da que la observada es", Zobs)

        tcrit = t.ppf(a/2, df=np.inf)
        print("Nos da que la esperada es", tcrit)

        if(Zobs < tcrit):
            print("\nComo la observada", Zobs, "es menor que la esperada", tcrit, "entonces se acepta la representatividad del programa")
        else:
            print("\nComo la observada", Zobs, "es mayor que la esperada", tcrit, "entonces se rechaza la representatividad del programa")

    def caso5(self):
        print("Caso 5. De una venta de autos tenemos nuestras muestras simuladas = 12,14,11,13,15,12,13,14,12,11,13,14,15,12,14 y las reales = 16,14,15,13,16,14,17,13,15,14,16,14,13. Determinar si es representativo. a = 4%")
        n1 = [12,14,11,13,15,12,13,14,12,11,13,14,15,12,14]
        n2 = [16,14,15,13,16,14,17,13,15,14,16,14,13]
        a = 0.04
        
        median1 = sum(n1)/len(n1)
        median2 = sum(n2)/len(n2)

        s2s = 0
        s2r = 0
        for i in range(len(n1)):
            s2s += (n1[i]-median1)**2

        s2s /= len(n1)-1

        for i in range(len(n2)):
            s2r += (n2[i]-median2)**2
        s2r /= len(n2)-1

        tobs = (median1 - median2)/(math.sqrt((len(n1)*s2s+len(n2)*s2r)/((len(n1)+len(n2))/2))*math.sqrt((1/len(n1))+(1/len(n2))))
        print("Nos da que la observada es", tobs)

        tcrit = t.ppf(a/2, (len(n1)+len(n2)-2))
        print("Nos da que la esperada es", tcrit)

        if(tobs < tcrit):
            print("\nComo la observada", tobs, "es menor que la esperada", tcrit, "entonces se acepta la representatividad del programa")
        else:
            print("\nComo la observada", tobs, "es mayor que la esperada", tcrit, "entonces se rechaza la representatividad del programa")

    def caso8(self):
        print("Caso 8. Tenemos un restaurante que tiene unas ventas simuladas = 250,248,241,244,251,248,250,253,251,244,244,242,237,236,235,240,241,240,280 y otras reales = 245,244,230,233,233,232,251,241,244,243,242,241,230,231,251,240,242,242,249,247,248,246,245,245 usar un error 5% para probar que no existe diferencia significativa entre ambas medias.")
        n1 = [245,244,230,233,233,232,251,241,244,243,242,241,230,231,251,240,242,242,249,247,248,246,245,245]
        n2 = [250,248,241,244,251,248,250,253,251,244,244,242,237,236,235,240,241,240,280]
        a = 0.05
        
        median1 = sum(n1)/len(n1)
        median2 = sum(n2)/len(n2)

        s2s = 0
        s2r = 0
        for i in range(len(n1)):
            s2s += (n1[i]-median1)**2

        s2s /= len(n1)-1

        for i in range(len(n2)):
            s2r += (n2[i]-median2)**2
        s2r /= len(n2)-1

        tobs = (median1 - median2)/math.sqrt((s2s/len(n1))+(s2r/len(n2)))
        print("Nos da que la observada es", tobs)

        w1 = s2s/len(n1)
        w2 = s2r/len(n2)
        t1 = (t.ppf(a/2, len(n1)-1))
        t2 = (t.ppf(a/2, len(n2)-1))
        tcrit = (w1*t1+w2*t2)/(w1+w2)
        print("Nos da que la esperada es", tcrit)

        if(tobs < tcrit):
            print("\nComo la observada", tobs, "es menor que la esperada", tcrit, "entonces se acepta la representatividad del programa")
        else:
            print("\nComo la observada", tobs, "es mayor que la esperada", tcrit, "entonces se rechaza la representatividad del programa")

if __name__ == "__main__":
    validacion = validacion()
    validacion.main()
    validacion

