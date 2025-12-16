import csv
import pandas as pd
import DistGenerator as DG

import math
from scipy.stats import chi2
from scipy.stats import ksone

#from scipy.stats import chi2
def truncate(number, trunc:int):
    #-----Método1-------
    #truncnumber=((number*10**trunc)//1)/10**trunc
    #-----Método2-------
    #n=str(number)
    #if '.' in n:
    #    integer, decimal=n.split('.')
    #    decimal=decimal[:trunc]
    #    truncnumber=float(f"{integer}.{decimal}")
    #-----Método3-------
    truncnumber=round(number,trunc)
    return truncnumber
def isfloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False
class DataProcessor:
    #Que puede hacer:
    # 0. Definir cuantas clases quiero procesar los datos -- Ya esta?
    #    (podria poner si tiene que ser agrupados o no agrupados) 
    # 1. Procesar los datos en bruto, crear la tabla de frecuencias,
    #    si los datos son agrupados, sacar su marca de clase
    # 2. Calcular la media, varianza y desviación estándar, en función si son agrupados o no.
    def __init__(self, Archive, classes:int): #Define numclasses and Dataset for processing
        self.Archive=Archive
        self.classes=classes
    def readDataColumn(self, column:int): #Read a column from the archived dataset
        Data=[]
        with self.Archive:
            Reader = csv.reader(self.Archive)
            for row in Reader:
                if(isfloat(row[column])):
                    Data.append(row[column])
        Data.pop(0) #Esto elimina el título el cual no nos interesa
        return Data
    def classifyData(self, Data, Trunc:int, MinValue:float, MaxValue:float, Mode:str): #Create a DataFrame with classes for processing
        RawTable={} #Datos para la tabla de freq final
        MarkTable={} #Datos en marca de clase para procesar (si son agrupados)
        DataTable={} #Datos clasificados en bruto
        InferiorL=[]
        SuperiorL=[]
        Range = MaxValue-MinValue #El rango de la muestra a evaluar
        TruncLimit=1/10**Trunc #Lo usamos para datos continuos.
        #Inicializar algunas variables
        #1.1 Define the classes
        for Class in range(self.classes):
            #Hay que hacer una diferenciación según el modo (quantity, discrete, continous)
            if Mode=="quantity":
                if Class<=MaxValue:
                    Field=str(Class)
                    RawTable[Field]=[0]
                    MarkTable[Field]=[0]
                    DataTable[Field]=[]
            else:
                if Mode=="discrete" and Range/self.classes>=2:
                    MinClass=truncate((Class/self.classes)*Range+MinValue,0) #Limite inferior de clase
                    if(Class!=range(self.classes)[-1]):
                        MaxClass=truncate(((((Class+1)/self.classes)*Range+MinValue)-1),0) #Limite superior de clase
                    else:
                        MaxClass=truncate(((((Class+1)/self.classes)*Range+MinValue)),0) #Limite superior de clase
                elif Mode=="continous":
                    MinClass=truncate((Class/self.classes)*Range+MinValue,Trunc) #Limite inferior de clase
                    if(Class!=range(self.classes)[-1]):
                        MaxClass=truncate((((Class+1)/self.classes)*Range+MinValue),Trunc)-TruncLimit #Limite superior de clase
                    else:
                        MaxClass=truncate((((Class+1)/self.classes)*Range+MinValue),Trunc) #Limite superior de clase
                Field=str(MinClass)+"-"+str(MaxClass)
                RawTable[Field]=[0]
                MarkTable[(MinClass+MaxClass)/2]=[0]
                DataTable[Field]=[]
                InferiorL.append(MinClass)
                SuperiorL.append(MaxClass)
        #1.2 Put and count data on the table
        for data in Data:
            for Class in range(self.classes):
                if Mode=="quantity":
                    if(float(data)==Class):
                        RawTable[str(Class)][0]+=1
                        MarkTable[str(Class)][0]+=1
                        DataTable[str(Class)].append(data)
                        break
                elif(InferiorL[Class]<=float(data)<=SuperiorL[Class]):
                    RawTable[str(InferiorL[Class])+"-"+str(SuperiorL[Class])][0]+=1
                    MarkTable[(InferiorL[Class]+SuperiorL[Class])/2][0]+=1
                    DataTable[str(InferiorL[Class])+"-"+str(SuperiorL[Class])].append(data)
                    break
        #Create de dataframe
        DataF=pd.DataFrame(RawTable, index=['FO'])
        DataM=pd.DataFrame(MarkTable, index=['FO'])
        return {1:[DataF,DataM],"ilimits":InferiorL,"slimits":SuperiorL}
    def calculateAverage(self, DataFrame:pd.DataFrame, Trunc:int, Mode:str):
        ObservedF='FO'
        Acum=0.0
        TAcum=0.0
        MClasses=DataFrame.columns
        #print(MClasses)
        for MClass in MClasses:
            TAcum+=DataFrame.loc[ObservedF,MClass]
            Acum+=DataFrame.loc[ObservedF,MClass]*float(MClass)
        Average=truncate(Acum/TAcum, Trunc)
        return Average
    def calculateVarianceStdDeviation(self, DataFrame:pd.DataFrame, Average:float, Trunc:int, Mode:str):
        ObservedF='FO'
        Acum=0.0
        TAcum=0.0
        MClasses=DataFrame.columns
        #print(MClasses)
        for MClass in MClasses:
            TAcum+=DataFrame.loc[ObservedF,MClass]
            Acum+=((float(MClass)-Average)**2)*DataFrame.loc[ObservedF,MClass]
        Variance=truncate(Acum/(TAcum-1), Trunc)
        StdDeviation=truncate(math.sqrt(Variance), Trunc)
        return {"s2":Variance, "s":StdDeviation}
    def calculateSampleSize(self, DataFrame:pd.DataFrame):
        ObservedF='FO'
        TAcum=0
        MClasses=DataFrame.columns
        for MClass in MClasses:
            TAcum+=DataFrame.loc[ObservedF,MClass]
        return TAcum
class ChiTest: 
    #Etapa I: Construcción
    # Requisitos: Tenemos que tener una tabla de frecuencias, 
    # 1. Tener las frecuencias como F. O. 
    # 2. Calcular las probabilidades teóricas según la distribución que quiero probar
    # 3. Sacara las F. E. multiplicando lo anterior por el tamaño de muestra (me lo retorna DataProcessor)
    # 
    #Etapa II: Chi2
    # Requisitos: Asignar un margen de rechazo al experimento
    # 0. Si la frecuencia es menor a 5, se fusiona las clases que sean necesarias 
    # (tengo un algoritmo para eso), en base a un codigo de formato de tablas
    # 1. Calcular la chi2 por cada clase
    # 2. Sumar todo las chi2 para tener la Chi2 Obs
    # 3. Sacar la Chi2 Teo
    # 4. Sacar conclusiones de aceptación y rechazo
    def __init__(self, DataFrame:pd.DataFrame, alpha:float):
        self.alpha=alpha
        self.DataFrame=DataFrame
        self.idealF=5
    def analyzeData(self, inferiorlimits:list[int], superiorlimits:list[int], Mode:str):
        isFinished=False
        Iterations=0
        FreqObs='FO'
        while not isFinished:
            isFinished=True
            Classes=self.DataFrame.columns
            for index in range(len(Classes)):
                if(self.DataFrame.loc[FreqObs,Classes[index]]<self.idealF):
                    #Case 1:Fuse the next Class with the current
                    isFinished=False
                    if(index!=len(Classes)-1):
                        Iterations+=1
                        self.fuseClass(Classes[index], Classes[index+1], Mode)
                        try:
                            superiorlimits.remove(superiorlimits[index])
                            inferiorlimits.remove(inferiorlimits[index+1])
                        except IndexError:
                            pass
                        #self.DataFrame=update
                        print("Iteración ",Iterations)
                        print(self.DataFrame)
                        break
                    #Case 2:Fuse the previous Class with the current
                    else:
                        Iterations+=1
                        self.fuseClass(Classes[index], Classes[index-1], Mode)
                        try:
                            inferiorlimits.remove(inferiorlimits[index])
                            superiorlimits.remove(superiorlimits[index-1])
                        except IndexError:
                            pass
                        #self.DataFrame=update
                        print("Iteración ",Iterations)
                        print(self.DataFrame)
                        break
        else:
            isFinished=True
        return self.DataFrame
    def fuseClass(self, CurrClass:str, Class:str, Mode:str):
        newClassName=None
        if Mode=="quantity":
            newClassName=str(CurrClass)+','+(Class)
        elif Mode=="discrete" or Mode=="continous":
            newClassName=str(CurrClass)+'-'+(Class)
        self.DataFrame=self.mergesumClass(CurrClass, Class, newClassName)
        return self.DataFrame
    def mergesumClass(self, CurrClass:str, Class:str, newClassName: str):
        self.DataFrame[CurrClass]+=self.DataFrame[Class]
        self.DataFrame.rename(columns={CurrClass:newClassName}, inplace=True)
        self.DataFrame.drop(columns=[Class], inplace=True)
        return self.DataFrame
    def calculateProbabilities(self, inferiorlimits:list[int], superiorlimits:list[int], a, b, Trunc, distribution:str="normal"):
        MClasses=self.DataFrame.columns
        nrm=DG.NormalDistribution(a,b)
        xp=DG.ExponencialDistribution(a)
        ps=DG.PoissonDistribution(a)
        if distribution=="normal":
            Zinf=[]
            PZi=[]
            PZa=[]
            print("Calculando probabilidad teórica normal...")
            for iL in inferiorlimits:
                zinf=truncate((iL-a)/b, Trunc)
                zi=truncate(nrm.getinPDistribution((iL)), Trunc)
                Zinf.append(zinf)
                PZi.append(zi)
            zil=truncate(nrm.getinPDistribution(superiorlimits[-1]), Trunc)
            self.DataFrame.loc["Zi"]=Zinf
            self.DataFrame.loc["P(Zi)"]=PZi
            print(self.DataFrame)
            #Get areas of probability
            print("Calculando áreas de probabilidad teórica normal...")
            for i in range(len(inferiorlimits)-1):
                z=PZi[i+1]-PZi[i]
                PZa.append(z)
            zl=zil-PZi[-1]
            PZa.append(zl)
            self.DataFrame.loc["P(Z)"]=PZa
            print(self.DataFrame)
        elif distribution=="exponential":
            Exp=[]
            for MClass in MClasses:
                SubMClasses=MClass.split(',')
                expsum=0.0
                for SubMClass in SubMClasses:
                    exp=truncate(xp.getinPDensity(float(SubMClass)),Trunc)
                    expsum+=exp
                Exp.append(expsum)
            self.DataFrame.loc["P(Exp)"]=Exp
            print("Calculando probabilidad teórica exponencial...")
            print(self.DataFrame)
        elif distribution=="Poisson":
            Pos=[]
            for MClass in MClasses:
                SubMClasses=MClass.split(',')
                possum=0.0
                for SubMClass in SubMClasses:
                    pos=truncate(ps.getinPDensityC(float(SubMClass)),Trunc)
                    possum+=pos
                Pos.append(possum)
            self.DataFrame.loc["P(Pos)"]=Pos
            print("Calculando probabilidad teórica de Poisson...")
            print(self.DataFrame)
        return self.DataFrame
    def calculateExpectedFreqs(self, sample:int, distribution:str="normal"):
        DPDict={"normal":"P(Z)", "exponential":"P(Exp)","Poisson":"P(Pos)"}
        MClasses=self.DataFrame.columns
        ExpectedF=[]
        print("Calculando la frecuencia esperada...")
        for MClass in MClasses:
            eF=self.DataFrame.loc[DPDict[distribution],MClass]*sample
            ExpectedF.append(round(eF))
        self.DataFrame.loc["FE"]=ExpectedF
        print(self.DataFrame)
        return self.DataFrame
    def doSquareXTest(self, Trunc:int):
        ExpectedF='FE'
        ObservedF='FO'
        SquareChi=0
        SChi=[]
        for Class in self.DataFrame:
            ExF=self.DataFrame.loc[ExpectedF,Class]
            ObF=self.DataFrame.loc[ObservedF,Class]
            schi=truncate(((ObF-ExF)**2)/ExF, Trunc)
            SChi.append(schi)
        self.DataFrame.loc["X**2"]=SChi
        print("Calculando la X**2 observada...")
        print(self.DataFrame)
        for schi in SChi:
            SquareChi+=schi
        print("La X**2 observada es "+str(SquareChi))
        return SquareChi
    def isAccepted(self, ObsSquareChi):
        NumClasses=len(self.DataFrame.columns)
        DegFreedom=NumClasses-1
        #Theoretical chi2
        TSChi=chi2.isf(self.alpha,df=DegFreedom) #Use of SciPy for calculate the theoretical X**2
        print("La X**2 teorica es "+str(TSChi))
        if(ObsSquareChi<TSChi):
            return True
        else:
            return False
class KolmogorovSmirnovTest:
    #Etapa I: Construcción
    # Requisitos: Tenemos que tener una tabla de frecuencias
    # 1. Sacar las probabilidades de las frecuencias según el tamaño de la muestra (me lo retorna DataProcessor)
    # 1.5 Sacar las acumuladas de dichas probabilidades
    # 2. Calcular las probabilidades teóricas según la distribución que quiero probar 
    #   (voy a tener que hacer un cálculo adicional si quiero probar que es normal).
    # 2.5 Calcular las acumuladas de dichas probabilidades
    #Etapa II: La Prueba
    # 1. Sacar la D de cada clase
    # 2. Hallar el máximo de las D
    # 3. Sacar la D teórica (me queda a deber)
    # 4. Sacar conclusiones de aceptación y rechazo
    def __init__(self, DataFrame:pd.DataFrame, sample:int, alpha:float):
        self.alpha=alpha
        self.sample=sample
        self.DataFrame=DataFrame
    def getobsProbabilities(self,Trunc:int):
        MClasses=self.DataFrame.columns
        Prob=[]
        for MClass in MClasses:
            p=truncate((self.DataFrame.loc["FO",MClass]/self.sample),Trunc)
            Prob.append(p)
        self.DataFrame.loc["p(x)"]=Prob
    def calculateProbabilities(self, inferiorlimits:list[int], superiorlimits:list[int], a, b, Trunc, distribution:str="normal"):
        MClasses=self.DataFrame.columns
        nrm=DG.NormalDistribution(a,b)
        xp=DG.ExponencialDistribution(a)
        ps=DG.PoissonDistribution(a)
        if distribution=="normal":
            Zinf=[]
            PZi=[]
            PZa=[]
            print("Calculando probabilidad teórica normal...")
            for iL in inferiorlimits:
                zinf=truncate((iL-a)/b, Trunc)
                zi=truncate(nrm.getinPDistribution((iL)), Trunc)
                Zinf.append(zinf)
                PZi.append(zi)
            zil=truncate(nrm.getinPDistribution(superiorlimits[-1]), Trunc)
            self.DataFrame.loc["Zi"]=Zinf
            self.DataFrame.loc["p(Zi)"]=PZi
            print(self.DataFrame)
            #Get areas of probability
            print("Calculando áreas de probabilidad teórica normal...")
            for i in range(len(inferiorlimits)-1):
                z=PZi[i+1]-PZi[i]
                PZa.append(z)
            zl=zil-PZi[-1]
            PZa.append(zl)
            self.DataFrame.loc["p(Z)"]=PZa
            print(self.DataFrame)
        elif distribution=="exponential":
            Exp=[]
            for MClass in MClasses:
                SubMClasses=MClass.split(',')
                expsum=0.0
                for SubMClass in SubMClasses:
                    exp=truncate(xp.getinPDensity(float(SubMClass)),Trunc)
                    expsum+=exp
                Exp.append(expsum)
            self.DataFrame.loc["p(Exp)"]=Exp
            print("Calculando probabilidad teórica exponencial...")
            print(self.DataFrame)
        elif distribution=="Poisson":
            Pos=[]
            for MClass in MClasses:
                SubMClasses=MClass.split(',')
                possum=0.0
                for SubMClass in SubMClasses:
                    pos=truncate(ps.getinPDensityC(float(SubMClass)),Trunc)
                    possum+=pos
                Pos.append(possum)
            self.DataFrame.loc["p(Pos)"]=Pos
            print("Calculando probabilidad teórica de Poisson...")
            print(self.DataFrame)
        return self.DataFrame
    def calculateAcumulated(self,Row:str,AcumRow:str):
        MClasses=self.DataFrame.columns
        Acum=[]
        acum=0.0
        for MClass in MClasses:
            acum+=self.DataFrame.loc[Row,MClass]
            Acum.append(acum)
        self.DataFrame.loc[AcumRow]=Acum
        return self.DataFrame
    def doKolmogorovSmirnovTest(self,Acum1:str,Acum2:str,Trunc:int):
        MClasses=self.DataFrame.columns
        Do=[]
        for MClass in MClasses:
            d=abs(self.DataFrame.loc[Acum1,MClass]-self.DataFrame.loc[Acum2,MClass])
            Do.append(d)
        self.DataFrame.loc["D"]=Do
        print("Calculando la D observada...")
        print(self.DataFrame)
        #Get the maximum D
        Dmax=Do[0]
        for dx in Do:
            if dx>Dmax:
                Dmax=dx
        print("La mayor D observada es "+str(truncate(Dmax,4)))
        return truncate(Dmax,4)
    def isAccepted(self,ObsD):
        #Theoretical D
        Da=ksone.isf(self.alpha,self.sample)
        print("La D critica es "+str(Da))
        if(ObsD<Da):
            return True
        else:
            return False
version="Beta 1.0"
def ExecTest():
    isIncorrect=True
    #Inicializar
    File=None
    Col=0
    Classes=0
    Mode="-"
    Comport="-"
    Range=[]
    Alpha=1
    print("Bienvenido a la prueba de comportamientos NO UNIFORMES "+version)
    try:
        while(isIncorrect==True):
            try:
                File=open(input("Ingrese el nombre del archivo a analizar: "), 'r')
                isIncorrect=False
            except FileNotFoundError:
                print("El archivo no existe, intente de nuevo.")
                isIncorrect=True
        isIncorrect=True
        while(isIncorrect==True):
            try:
                Col=int(input("Ingrese a que columna quiere dirigir el análisis: "))
                isIncorrect=False
            except:
                print("El número de columna debe ser entero, intente otra vez.")
                isIncorrect=True
        isIncorrect=True
        while(isIncorrect==True):
            try:
                Classes=int(input("Ingrese el número de clases con lo que va a realizar la prueba: "))
                isIncorrect=False
            except ValueError:
                print("El número de clases debe ser entero, intente otra vez.")
                isIncorrect=True
        dt=DataProcessor(File, Classes)
        data=dt.readDataColumn(Col)
        #print(data)
        isIncorrect=True
        while(isIncorrect==True):
            Mode=input("Ingrese el modo de análisis de datos de las siguientes opciones: \n 1) No agrupado, escriba \"quantity\".\n 2) Discreto, escriba \"discrete\".\n 3) Continuo, escriba \"continous\".\n")
            if(Mode in ["quantity", "discrete", "continous"]):
                isIncorrect=False
            else:
                print("Valor no válido, intente de nuevo")
        isIncorrect=True
        while(isIncorrect==True):
            try:
                minimo=float(data[0])
                maximo=float(data[0])
                Range=input("Define el valor mínimo y máximo para recabar la muestra Formato:'(Min-Max)' o '(num1-num2)': ").split('-')
                if(Range[0]=='Min'):
                    for element in data:
                        if float(element)<minimo:
                            minimo=float(element)
                    Range[0]=minimo
                if(Range[1]=='Max'):
                    for element in data:
                        if float(element)>maximo:
                            maximo=float(element)
                    Range[1]=maximo
                Range[0]=float(Range[0])
                Range[1]=float(Range[1])
                print(Range)
                isIncorrect=False
            except ValueError:
                print("Valor no válido, intente de nuevo")
                isIncorrect=True
        isIncorrect=True
        while(isIncorrect==True):
            Comport=input("Ingrese el comportamiento que quiera evaluar hay de las siguientes opciones: \n 1) Normal (default) - Escriba \"normal\" para evaluar.\n 2) Exponencial - Escriba \"exponential\" para evaluar.\n 3) Poisson - Escriba \"Poisson\" para evaluar.\n")
            if(Comport in ["normal", "exponential", "Poisson"]):
                isIncorrect=False
            else:
                print("Valor no válido, intente de nuevo")
        isIncorrect=True
        while(isIncorrect==True):
            try:
                Alpha=float(input("Ingrese el margen de rechazo de la prueba: "))
                if(0<Alpha<1):
                    isIncorrect=False
                else:
                    print("Ingrese por favor un número en el intervalo (0,1). Intente de nuevo")
                    isIncorrect=True
            except ValueError:
                print("Ingrese por favor un número en el intervalo (0,1), intente de nuevo.")
                isIncorrect=True
        resp1=dt.classifyData(data, 4, Range[0], Range[1], Mode)
        FreqTable=resp1[1][0]
        MarkTable=resp1[1][1]
        print("Tabla de frecuencias original")
        print(FreqTable)
        print("Tabla de frecuencias en marcas de clase")
        print(MarkTable)
        n=dt.calculateSampleSize(MarkTable)
        avg=dt.calculateAverage(MarkTable, 4, Mode)
        s=dt.calculateVarianceStdDeviation(MarkTable, avg, 4, Mode)
        var=s["s2"]
        sd=s["s"]
        print("El tamaño de la muestra es: ",n)
        print("El promedio es:", avg)
        print("La varianza es:", var)
        print("La desviación estándar es:", sd)
        if(n>100):
            x2=ChiTest(MarkTable,Alpha)
            #print(resp1[2])
            x2.analyzeData(resp1["ilimits"], resp1["slimits"], Mode)
            x2.calculateProbabilities(resp1["ilimits"], resp1["slimits"],avg,sd,4,Comport)
            x2.calculateExpectedFreqs(n,Comport)
            oChi2=x2.doSquareXTest(4)
            veredict=x2.isAccepted(oChi2)
            if(veredict is True):
                ProbVoc={"normal":"normal","exponential":"exponencial","Poisson":"Poisson"}
                print("Se puede ACEPTAR que la muestra presenta un comportamiento "+str(ProbVoc[Comport])+" a un margen de rechazo de "+str(Alpha))
            else:
                ProbVoc={"normal":"normal","exponential":"exponencial","Poisson":"Poisson"}
                print("Se puede RECHAZAR que la muestra presenta un comportamiento "+str(ProbVoc[Comport])+" a un margen de rechazo de "+str(Alpha))
        else:
            DisName={"normal":"p(Z)","exponential":"p(Exp)","Poisson":"p(Pos)"}
            AcumName={"normal":"P(Z)","exponential":"P(Exp)","Poisson":"P(Pos)"}
            ks=KolmogorovSmirnovTest(MarkTable,n,Alpha)
            ks.getobsProbabilities(4)
            ks.calculateAcumulated("p(x)","P(x)")
            ks.calculateProbabilities(resp1["ilimits"], resp1["slimits"],avg,sd,4,Comport)
            ks.calculateAcumulated(DisName[Comport],AcumName[Comport])
            DMax=ks.doKolmogorovSmirnovTest("P(x)",AcumName[Comport],4)
            veredict=ks.isAccepted(DMax)
            if(veredict is True):
                ProbVoc={"normal":"normal","exponential":"exponencial","Poisson":"Poisson"}
                print("Se puede ACEPTAR que la muestra presenta un comportamiento "+str(ProbVoc[Comport])+" a un margen de rechazo de "+str(Alpha))
            else:
                ProbVoc={"normal":"normal","exponential":"exponencial","Poisson":"Poisson"}
                print("Se puede RECHAZAR que la muestra presenta un comportamiento "+str(ProbVoc[Comport])+" a un margen de rechazo de "+str(Alpha))
    except KeyboardInterrupt:
        print("\nPrograma cerrado.")
if __name__=="__main__":
    ExecTest()