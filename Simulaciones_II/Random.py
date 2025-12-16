from multipledispatch import dispatch
class Random:
    seed=0
    a=2
    c=1
    var=2017
    @dispatch(int)
    def __init__(self, seed):
        """
        Constructor de la clase para instanciar los métodos para generar números pseudo-aleatorios.

        Parámetros
        ----------
        seed : int 
            semilla del generador.
        a : int
            multiplicador del generador.
        c : int
            desplazador del generador.
        var : int
            El rango de valores generador [0,1).
        """
        self.seed=seed
        self.var
        #Variables para Set/Get
        self.a
        self.c
    @dispatch(int,int)
    def __init__(self, seed, var):
        """
        Constructor de la clase para instanciar los métodos para generar números pseudo-aleatorios.

        Parámetros
        ----------
        seed : int 
            semilla del generador.
        a : int
            multiplicador del generador.
        c : int
            desplazador del generador.
        var : int
            El rango de valores generador [0,1).
        """
        self.seed=seed
        self.var=var
        #Variables para Set/Get
        self.a
        self.c
    #Getters/Setters
    def setSeed(self, newSeed):
        self.seed=newSeed
    def getSeed(self):
        return self.seed
    def setVar(self, newVar):
        self.var=newVar
    def getVar(self):
        return self.var
    def setA(self,newA):
        self.a=newA
    def getA(self):
        return self.a
    def setC(self,newC):
        self.c=newC
    def getC(self):
        return self.c
    def genNextInt(self):
        """
        Genera el siguiente número aleatorio
        """
        if(self.a<2 or self.a>self.var):
            print("Error. Valor de a no válido.")
        if(self.c<0 or self.c>self.var):
            print("Error. Valor de c no válido.")
        if(self.seed<0 or self.seed>self.var):
            print("Error. Valor de semilla no válido.")
        if(2<=self.a<self.var and 0<=self.c<self.var and 0<=self.seed<self.var):
            try:
                newSeed=(self.a*self.seed+self.c)%self.var
            except ValueError:
                print("Error. Valor de var no válido.")
            self.setSeed(newSeed)
            return newSeed
    @dispatch()
    def genNextDecimal(self):
        """
        Genera un flotante entre [0,1)
        """
        number=self.genNextInt()/self.var
        return number
    @dispatch(int)
    def genNextDecimal(self, precission:int):
        """
        Genera un flotante truncado entre [0,1) dada una precisión dada
        """
        num=self.genNextInt()/self.var
        number=((num*(10**precission))//1)/10**precission
        return number
    def genNextIntArray(self, N:int):
        randomArray=[]
        for i in range(N):
            rand=self.genNextInt()
            randomArray.append(rand)
        return randomArray
    @dispatch(int)
    def genNextDecimalArray(self, N:int):
        randomArray=[]
        for i in range(N):
            rand=self.genNextDecimal()
            randomArray.append(rand)
        return randomArray
    @dispatch(int,int)
    def genNextDecimalArray(self, N:int, precission:int):
        randomArray=[]
        for i in range(N):
            rand=self.genNextDecimal(precission)
            randomArray.append(rand)
        return randomArray