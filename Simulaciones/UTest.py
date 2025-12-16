import csv
import pandas as pd
from scipy.stats import chi2

def readDataColumn(Archive, column:int): #Read a column of a archived dataset
    Data=[]
    with Archive:
        Reader = csv.reader(Archive)
        for row in Reader:
            Data.append(row[column])
    return Data
def classifyData(Data, NumClasses:int, Trunc:int, MinValue, MaxValue): #Create a DataFrame with classes for processing
    #Order the data
    RawTable={}
    DataTable={}
    InferiorL=[]
    SuperiorL=[]
    Range = MaxValue-MinValue
    IdealNumber = len(Data)/NumClasses
    TruncLimit=1/10**Trunc
    #1.1 Create classes
    for Class in range(NumClasses):
        MinClass=(Class/NumClasses)*Range #Limite inferior de clase
        MaxClass=(((((Class+1)/NumClasses)*Range)-TruncLimit)*10**Trunc//1)/10**Trunc #Limite superior de clase
        Field=str(MinClass)+"-"+str(MaxClass)
        RawTable[Field]=[IdealNumber,0]
        DataTable[Field]=[]
        InferiorL.append(MinClass)
        SuperiorL.append(MaxClass)
    #1.2 Put and count data on the table
    for data in Data:
        for Class in range(NumClasses):
            if(InferiorL[Class]<float(data)<SuperiorL[Class]):
                RawTable[str(InferiorL[Class])+"-"+str(SuperiorL[Class])][1]+=1
                DataTable[str(InferiorL[Class])+"-"+str(SuperiorL[Class])].append(data)
                break
    #2.1 Prep the datatable
    MaxLen=max(len(c) for c in DataTable.values())
    for Class in DataTable:
        if len(DataTable[Class])<MaxLen:
            DataTable[Class].extend([None]*(MaxLen-len(DataTable[Class])))
    #Create a dataframe
    DataF=pd.DataFrame(RawTable, index=["FE","FO"])
    DataF2=pd.DataFrame(DataTable, index=range(1,MaxLen+1))
    return {1:DataF, 2:DataF2, "ilimits":InferiorL, "slimits":SuperiorL}
def analyzeData(DataFrame:pd.DataFrame, FO, IdealF:float, fuseClass): #Simplify the DataFrame for SquareChiTest
    isFinished=False
    Iteraciones=0
    while isFinished==False:
        Classes=DataFrame.columns #Get the columns of the current iteration
        for index in range(len(Classes)):
            if(DataFrame.loc[FO,Classes[index]]<IdealF):
                #Case 1:Fuse the next Class with the current
                if(index!=len(Classes)-1):
                    Iteraciones+=1
                    update=fuseClass(DataFrame, Classes[index], Classes[index+1])
                    DataFrame=update
                    print("Iteración ",Iteraciones)
                    print(DataFrame)
                    break
                #Case 2:Fuse the previous Class with the current
                else:
                    Iteraciones+=1
                    update=fuseClass(DataFrame, Classes[index], Classes[index-1])
                    DataFrame=update
                    print("Iteración ",Iteraciones)
                    print(DataFrame)
        else:
            isFinished=True
    return DataFrame
def fuseClass(DataFrame:pd.DataFrame, CurrClass:str, Class:str):
    ILCurrC, SLCurrC = map(float, CurrClass.split('-'))
    ILCl, SLCl = map(float, Class.split('-'))
    newClassName=str(min(ILCurrC,ILCl))+'-'+str(max(SLCurrC,SLCl))
    newDataFrame=mergesumClass(DataFrame, CurrClass, Class, newClassName)
    return newDataFrame
def mergesumClass(DataFrame:pd.DataFrame, CurrClass:str, Class:str, newClassName: str):
    DataFrame[CurrClass]+=DataFrame[Class]
    DataFrame.rename(columns={CurrClass:newClassName}, inplace=True)
    DataFrame.drop(columns=[Class], inplace=True)
    return DataFrame
def dosSquareXTest(DataFrame:pd.DataFrame):
    ExpectedF="FE"
    ObservedF="FO"
    SquareChi=0
    SChi=[]
    for Class in DataFrame:
        ExF=DataFrame.loc[ExpectedF,Class]
        ObF=DataFrame.loc[ObservedF,Class]
        #Calculate class squarechi
        schi=(ObF-ExF)**2/ExF
        SChi.append(schi)
    DataFrame.loc["X"]=SChi
    print("Calculando la X**2 observada...")
    print(DataFrame)
    for schi in SChi:
        SquareChi+=schi
    print("La X**2 observada es "+str(SquareChi))
    return {"table":DataFrame, "X**2":SquareChi}
def isAccepted(DataFrame, ObservedSquareChi, Tolerancy): #Apply the X**2 comparing the theoretical X**2 
    NumClasses=len(DataFrame.columns)
    DegFreedom=NumClasses-1
    TSChi=chi2.isf(Tolerancy,df=DegFreedom) #Use of SciPy for calculate the theoretical X**2
    print("La X**2 teorica es "+str(TSChi))
    if(ObservedSquareChi<TSChi):
        return True
    else:
        return False
if __name__=="__main__":
    version="1.2"
    esIncorrecto=True
    print("Bienvenido a la prueba de uniformidad ",version)
    try:
        while (esIncorrecto==True):
            try:
                tolerancia=float(input("Ingrese la tolerancia(rechazo) que desee para el experimento: "))
                if (0<tolerancia<1):
                    esIncorrecto=False
                else:
                    print("Ingrese por favor un número en el intervalo [0,1).")
                    esIncorrecto=True
            except ValueError:
                print("Ingrese por favor un número en el intervalo [0,1), en lugar de letras.")
                esIncorrecto=True
        test=open("Datos.csv",'r')
        tables=classifyData(readDataColumn(test,1), 5, 4, 0, 1)
        print(tables[2]) #Imprime la tabla con los datos
        FreqTable=tables[1]
        print("Tabla de frecuencias original: ")
        print(FreqTable) #Imprime la tabla con las frecuencias
        UltimateTable=analyzeData(FreqTable, "FO", 5.0, fuseClass)
        res=dosSquareXTest(UltimateTable)
        if(isAccepted(UltimateTable, res["X**2"], tolerancia)):
            print("La muestra de números pseudoaleatorios SI es uniforme a una tolerancia de "+str(tolerancia))
        else:
            print("La muestra de números pseudoaleatorios NO es uniforme a una tolerancia de "+str(tolerancia))
    except KeyboardInterrupt:
        print("\nPrograma cerrado.")
    except NameError:
        print("La tolerancia no está definida.")