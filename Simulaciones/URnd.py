import csv
seed = 0
n_seed = 0
def URNG_0(n, seed, factor, displacement, quantity): #Método recursivo para generar números aleatorios
    newseed = (factor*seed+displacement)%quantity
    if n > 1:
        print(newseed)
        return URNG_0(n-1, newseed, factor, displacement, quantity)
def NextURNG(factor, displacement, quantity): #Devuelve el siguiente número aleatorio 
    global seed, n_seed
    n_seed = (factor*seed+displacement)%quantity
    seed=n_seed
    return seed
def NextNURNG(N, factor, displacement, quantity): #Devuelve un array de N números aleatorios
    arrayres=[]
    for i in range(N):
        res=NextURNG(factor, displacement, quantity)
        print(res)
        arrayres.append(res)
    return arrayres
def NextNRangeURNG(N, factor, displacement, minvalue, maxvalue): #Devuelve un array de N números aleatorios desde un valor a otro
    arrayres=[]
    for i in range(N):
        res=NextURNG(factor, displacement, maxvalue-minvalue+2)+minvalue
        if (res>maxvalue):
            res=maxvalue
        print(res)
        arrayres.append(res)
    return arrayres
def truncate(number, trunc:int):
    truncnumber=((number*10**trunc)//1)/10**trunc
    return truncnumber
#fields2=["number,decimate"]
if __name__=="__main__":
    #Preparación de datos
    version = "1.0"
    t = 4
    print("Bienvenido al simulador de generador de números aleatorios con azar uniforme", version)
    print("Especificaciones del generador.\nN: Número de números a generar \nS: Semilla. \nM: Indica el factor de aleatoriedad.\nD: Indica el desplazamiento.\nR: Rango de los valores (0,R) que se pueden generar (Puedes poner un argumento adicional para valores (MIN,MAX)).")
    error=False #Flag
    try:
        while (error==False):
            try:
                inputA=input("Establezca los valores del generador (N, S, M, D, R): ").split(',')
                if any(int(inputA[i])>0 for i in range(len(inputA))):
                    if len(inputA)==5:
                        if (int(inputA[1])>int(inputA[4])):
                            print("El rango debe ser mayor que la semilla. Intente otra vez.")
                        elif(int(inputA[2])<2):
                            print("El factor debe ser menor o igual que 2. Intente otra vez.")
                        elif (int(inputA[2])>int(inputA[4])):
                            print("El rango debe ser mayor que su factor. Intente otra vez.")
                        elif (int(inputA[3])>int(inputA[4])):
                            print("El rango debe ser mayor al desplazamiento. Intente otra vez.")
                        else:
                            seed=int(inputA[1])
                            #Genero los números aleatorios
                            generatedNumbers = NextNURNG(int(inputA[0]),int(inputA[2]),int(inputA[3]),int(inputA[4]))
                            #Genera el CSV
                            Archive = open("Datos.csv", 'a',newline='')
                            #Se escriben y se generan los valores a tratar
                            with open("Datos.csv",'w',newline=''):
                                tempnumber=None
                                Writer = csv.writer(Archive,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                for number in generatedNumbers:
                                    decnumber=truncate((number/int(inputA[4])),4)
                                    arrnumber=int(truncate((number/int(inputA[4])),5)*10**5)
                                    if(decnumber<=0.5):
                                        tempnumber=0
                                    else:
                                        tempnumber=1
                                    Writer.writerow([str(number),str(decnumber),str(tempnumber),str(arrnumber).zfill(5)])
                            error=True
                    elif len(inputA)==6:
                        seed=int(inputA[1])
                        generatedNumbers = NextNRangeURNG(int(inputA[0]),int(inputA[2]),int(inputA[3]),int(inputA[4]),int(inputA[5]))
                        error=True
                else:
                    print("Tus especificaciones deben ser de números enteros positivos.")
            except ValueError:
                print("Los valores tienen que ser numéricos. Intente de nuevo.")
                error=False
    except KeyboardInterrupt:
        print("\nPrograma cerrado.")