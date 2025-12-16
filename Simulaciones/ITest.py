import math
import URnd as rd
import UTest as xt
import ATest as at
import pandas as pd
def classifyData(Data):
    NData=len(Data)
    #Final tables
    ObF={}
    DataTable={}
    #Temporary tables
    ExF={}
    #Classify data
    for data in Data:
        cat=matchCategory(data)
        if cat in ObF:
            ObF[cat]+=1
        else:
            ObF[cat]=0
            ObF[cat]+=1
        if cat in DataTable:
            DataTable[cat].append(data)
        else:
            DataTable[cat]=[]
            DataTable[cat].append(data)
    #Get the expected frequencies
    for Cat in Categories:
        ExF[Cat]=rd.truncate(Categories[Cat]*NData,4)
    #Prep DataTable
    MaxLen=max(len(c) for c in DataTable.values())
    for Class in DataTable:
        if len(DataTable[Class])<MaxLen:
            DataTable[Class].extend([None]*(MaxLen-len(DataTable[Class])))
    #Create the dataframes
    DataF=pd.DataFrame([ExF,ObF], index=["FE","FO"]).fillna(0)
    DataF2=pd.DataFrame(DataTable, index=range(1,MaxLen+1))
    return {1: DataF, 2:DataF2}
def sortAtRow(DataFrame:pd.DataFrame, IndexRow):
    SDataFrame=DataFrame.sort_values(by=IndexRow, axis=1, ascending=False)
    return SDataFrame
def matchCategory(digits:str):
    ocs=getDigitOcurrencies(digits)
    if (getOcurrenciesSubsets(ocs, 1)==5):
        return "Normal"
    elif (getOcurrenciesSubsets(ocs, 2)==1 and getOcurrenciesSubsets(ocs, 1)==3):
        return "Par"
    elif (getOcurrenciesSubsets(ocs, 2)==2):
        return "DoublePar"
    elif (getOcurrenciesSubsets(ocs, 3)==1 and getOcurrenciesSubsets(ocs, 1)==2):
        return "Triplet"
    elif (getOcurrenciesSubsets(ocs, 3)==1 and getOcurrenciesSubsets(ocs, 2)==1):
        return "FullHouse"
    elif (getOcurrenciesSubsets(ocs, 4)==1):
        return "Poker"
    elif (getOcurrenciesSubsets(ocs, 5)==1):
        return "Color"
def getDigitOcurrencies(digits:str):
    #Count ocurrence for each digit
    ocurrences=[]
    for i in range(10):
        ocurrencei=digits.count(str(i))
        if(ocurrencei>0):
            ocurrences.append(ocurrencei)
    return ocurrences
def getOcurrenciesSubsets(ocurrencies:list[int], category:int):
    subsets=ocurrencies.count(category)
    return subsets
def getCombs(C:int, K:int):
    combs=math.factorial(C)/(math.factorial(K)*math.factorial(C-K))
    return combs
Categories={
    "Normal":(10*9*7*6*5)/10**5,
    "Par":((10*1*9*8*7)/10**5)*getCombs(5,2),
    "DoublePar":((10*1*9*1*8)/10**5)*getCombs(5,2)*getCombs(3,2)*(1/2),
    "Triplet":((10*1*1*9*8)/10**5)*getCombs(5,3),
    "FullHouse":((10*1*1*9*1)/10**5)*getCombs(5,3)*getCombs(2,2),
    "Poker":((10*1*1*1*9)/10**5)*getCombs(5,4),
    "Color":(10*1*1*1*1)/10**5
    }
TCategories={
    "Normal":rd.truncate(Categories["Normal"],4),
    "Par":rd.truncate(Categories["Par"],4),
    "DoublePar":rd.truncate(Categories["DoublePar"],4),
    "Triplet":rd.truncate(Categories["Triplet"],4),
    "FullHouse":rd.truncate(Categories["FullHouse"],4),
    "Poker":rd.truncate(Categories["Poker"],4),
    "Color":rd.truncate(Categories["Color"],4)
}
if __name__=="__main__":
    version="1.0"
    isIncorrecto=True
    print("Bienvenido a la prueba de independencia (Viva México) ",version)
    try:
        try:
            while (isIncorrecto==True):
                tolerancia=float(input("Ingrese la tolerancia(rechazo) que desee para el experimento: "))
                if(0<tolerancia<1):
                    isIncorrecto=False
                else:
                    print("Ingrese por favor un número en el intervalo [0,1).")
            print()
        except ValueError:
            print("Ingrese por favor un número en el intervalo [0,1), en lugar de letras.")
        test3=open("Datos.csv")
        data=xt.readDataColumn(test3,3)
        #print(data)
        tables=classifyData(data)
        FeqTable=tables[1]
        print("Tabla de frecuencias original.")
        print(FeqTable)
        print("Analizando y preparando...")
        SFeqTable=sortAtRow(FeqTable,"FE")
        print(SFeqTable)
        UltimateTable=xt.analyzeData(SFeqTable,"FO",5, at.fuseClass)
        res=xt.dosSquareXTest(UltimateTable)
        if(xt.isAccepted(UltimateTable, res["X**2"], tolerancia)):
            print("La muestra de números pseudoaleatorios SI es independiente a una tolerancia de "+str(tolerancia))
        else:
            print("La muestra de números pseudoaleatorios NO es independiente a una tolerancia de "+str(tolerancia))
    except KeyboardInterrupt:
        print("\nPrograma terminado.")
    except NameError:
        print("La tolerancia no esta definida.")