from Random import Random
import math
from scipy.stats import norm

def truncate(number, trunc:int):
    truncnumber=((number*10**trunc)//1)/10**trunc
    return truncnumber
def getCombs(C:int, K:int):
    combs=math.factorial(C)/(math.factorial(K)*math.factorial(C-K))
    return combs
class ExponencialDistribution:
    average=0.0
    def __init__(self, average:float):
        self.average=average
    def getinPDensity(self, x:int|float):
        ImagefP=self.average*(math.e**(-self.average*x))
        return ImagefP
    def getinPDistribution(self, x:int|float):
        ImageFP=1-math.e**(-self.average*x)
        return ImageFP
    def getinPDistributionInverse(self, rnd:float):
        InverseFP=-math.log(1-rnd,math.e)/self.average
        return InverseFP
class PoissonDistribution:
    averagef=0
    def __init__(self,averagef:int):
        self.averagef=averagef
    def getinPDensity(self, k:int):
        ImagefP=((math.e**(-self.averagef))*(self.averagef**k))/math.factorial(k)
        return ImagefP
    def getinPDensityC(self,k:float):
        ImagefP=((math.e**(-self.averagef))*(self.averagef**k))/math.gamma(k+1)
        return ImagefP
    def getImagesinPDistribution(self,maxk:int):
        FunctionP={}
        Images=[]
        acc=0
        for i in range(maxk+1):
            acc+=self.getinPDensity(i)
            FunctionP[i]=acc
            Images.append(acc)
        #print("Imagenes")
        #print(Images)
        return {"func": FunctionP, "img":Images}
    def getinPDistributionInverse(self, rnd:float, maxk:int, trunc:bool=False, precission=None|int):
        FunctionP=self.getImagesinPDistribution(maxk)["img"]
        FunctionP.insert(0,0.0)
        lenght=len(FunctionP)
        if (trunc==True):
            temp=[]
            for i in range(lenght):
                temp=truncate(FunctionP[i],precission)
                FunctionP[i]=temp
        #print(FunctionP)
        for ki in range(lenght-1):
            if ki<lenght-2:
                if(FunctionP[ki]<=rnd<FunctionP[ki+1]):
                    #print(rnd)
                    return ki
            else:
                if(FunctionP[ki]<=rnd<=FunctionP[ki+1]):
                    return ki
class BinomialDistribution:
    sample=0
    sucessprob=0.0
    def __init__(self, sample:int, sucessprob:float):
        self.sample=sample
        self.sucessprob=sucessprob
    def getinPDensity(self, x:int):
        ImagefP=(getCombs(self.sample,x))*((self.sucessprob)**x)*((1-self.sucessprob)**(self.sample-x))
        print(getCombs(self.sample,x))
        return ImagefP
    def getinPDistributionInverseR(self, rnd:list):
        x=0
        for i in range(len(rnd)):
            if(rnd[i]>self.sucessprob):
                continue
            else:
                x+=1
        return x
class NormalDistribution:
    average=0.0
    standardD=0.0
    def __init__(self, average, standardD):
        self.average=average
        self.standardD=standardD
    def getinPDensity(self, x:float):
        ImagefP=(1/(self.standardD*math.sqrt(2*math.pi)))*(math.e**((-1/2)*((x-self.average)/self.standardD)**2))
        return ImagefP
    def getDesviation(self, x:float):
        Desviation=(x-self.average)/self.standardD
        return Desviation
    def getinPDistribution(self, x:float):
        ImageFP=norm.cdf(x, loc=self.average, scale=self.standardD)
        return ImageFP
    def getinPDistributionInverseR(self, rnd:list):
        SumRND=0.0
        numRND=len(rnd)
        for i in range(numRND):
            SumRND+=rnd[i]
        NormalZ=self.average+self.standardD*((SumRND-numRND/2)/(math.sqrt(numRND/12)))
        return NormalZ
def generate(sample:list, average:float, standardD:float, probsucess:float, sets:int):
    expD=ExponencialDistribution(average)
    posD=PoissonDistribution(average)
    bD=BinomialDistribution(0,probsucess)
    nD=NormalDistribution(average,standardD)
    lenght=len(sample)
    expG=[]
    posG=[]
    binG=[]
    norG=[]
    #Vars for analysis
    subset=[]
    subsets=[]
    for i in range(100):
        exp=expD.getinPDistributionInverse(sample[i])
        pos=posD.getinPDistributionInverse(sample[i],15,True,4)
        expG.append(truncate(exp,4))
        posG.append(pos)
    for i in range(lenght):
        if(i%sets==0):
            if len(subset)!=0:
                subsets.append(subset)
                subset=[]
        subset.append(sample[i])
    #print(subsets)
    for subset in subsets:
        bin=bD.getinPDistributionInverseR(subset)
        nor=nD.getinPDistributionInverseR(subset) 
        binG.append(bin)
        norG.append(truncate(nor,4))
    print("Valores generados en distribución exponencial.")
    print(expG)
    print("Valores generados en distribución de Poisson.")
    print(posG)
    print("Valores generados en distribución binomial.")
    print(binG)
    print("Valores generados en distribución normal.")
    print(norG)

if __name__=="__main__":
    rnd=Random(24)
    rnd.setVar(19857)
    rnd.setA(3)
    rnd.setC(1)
    sample=rnd.genNextDecimalArray(1000,4)
    print("Valores uniformes aleatorios:")
    print(sample)
    generate(sample, 5, 2.34, 0.02,10)


#print(expD.getinPDensity(3))
#print(expD.getinPDistribution(3))
#print(expD.getinPDistributionInverse(expD.getinPDistribution(3)))
#print(posD.getinPDensityC(2))
#print(posD.getinPDensity(2))
#print(posD.getImagesinPDistribution(15)["func"])
#print(posD.getinPDistributionInverse(0.9995, 15, True, 4))
#print(bD.getinPDistributionInverseR((0.34, 0.55, 0.56, 0.67, 0.33, 0.02)))
#print(nD.getinPDensity(63))
#print(nD.getinPDistribution(63))
#print(nD.getinPDistributionInverseR((0.34, 0.55, 0.56, 0.67, 0.33, 0.12)))
