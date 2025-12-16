import UTest as xt
import pandas as pd
def classifyData(Data, Trunc:int):
    #Finale tables
    DataF={}
    #Temporary tables
    TableFO={}
    TableFE={}
    Table0=countDataCategoryInARow(Data,'0','1')
    Table1=countDataCategoryInARow(Data,'1','0')
    DataF0=pd.DataFrame(Table0, index=[1])
    DataF1=pd.DataFrame(Table1, index=[1])
    print("Datos obtenidos durante el analisis...")
    print("Conteo de números menores que la media según la longitud de corrida.")
    print(DataF0)
    print("Conteo de números mayores que la media según la longitud de corrida.")
    print(DataF1)
    #2.1 Prep tables, case: Observed Frequency
    TableFO=Table0.copy()
    for index, value in Table1.items():
        if index in TableFO:
            TableFO[index]+=value
        else:
            TableFO[index]=value
    #2.2 Prep tables, case: Expected Frequency
    NumClasses=len(TableFO)
    for Class in range(NumClasses):
        TableFE[Class]=((((len(Data)-Class+3)/2**(1+Class))*10**Trunc)//1)/10**Trunc
    DataF=pd.DataFrame([TableFE, TableFO], index=["FE","FO"])
    return DataF
def countDataCategoryInARow(Data, Category:str, Limiter:str): #Count data according to a category between two limiters
    RawTable={}
    counterCategory=0
    counterlimits=0
    for data in Data:
        if (data==Limiter):
            counterlimits+=1
        if (0<counterlimits<2 and data==Category):
            counterCategory+=1
        elif(counterlimits>=2):
            counterlimits=1
            if(counterCategory in RawTable):
                RawTable[counterCategory]+=1
            else:
                RawTable[counterCategory]=0
                RawTable[counterCategory]+=1
            counterCategory=0
    for index in range(max(RawTable)+1):
        if not index in RawTable:
            RawTable[index]=0
    FinalRawTable=dict(sorted(RawTable.items()))
    return FinalRawTable
def fuseClass(DataFrame:pd.DataFrame, CurrClass:str, Class:str):
    #Set Name Class
    CurrClasses=str(CurrClass).split(',')
    newClassName=str(Class)
    for aClass in CurrClasses:
        newClassName+=(','+aClass)
    xt.mergesumClass(DataFrame, CurrClass, Class, newClassName)
    return DataFrame
    #Merge Classes
if __name__=="__main__":
    version="1.3"
    isIncorrecto=True
    print("Bienvenido a la prueba de aleatoriedad ",version)
    try:
        try:
            while (isIncorrecto==True):
                tolerancia=float(input("Ingrese la tolerancia(rechazo) que desee para el experimento: "))
                if (0<tolerancia<1):
                    isIncorrecto=False
                else:
                    print("Ingrese por favor un número en el intervalo [0,1).")
        except ValueError:
            print("Ingrese por favor un número en el intervalo [0,1), en lugar de letras")
        test2=open("Datos.csv",'r')
        data=xt.readDataColumn(test2, 2)
        #print(data)
        FreqTable=classifyData(data, 4)
        print("Tabla de frecuencias original: ")
        print(FreqTable)
        UltimateTable=xt.analyzeData(FreqTable, "FO", 5, fuseClass)
        res=xt.dosSquareXTest(UltimateTable)
        if(xt.isAccepted(UltimateTable, res["X**2"], tolerancia)):
            print("La muestra de números pseudoaleatorios SI es aleatoria a una tolerancia de "+str(tolerancia))
        else:
            print("La muestra de números pseudoaleatorios NO es aleatoria a una tolerancia de "+str(tolerancia))
    except KeyboardInterrupt:
        print("\nPrograma terminado.")
    except NameError:
        print("La tolerancia no esta definida.")