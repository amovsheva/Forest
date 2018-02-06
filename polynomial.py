class Polynomial:
    def __init__(self, list):
        self.__data = list
        self.__truncate()
        
    @property
    def data(self):
        return self.__data
    
    def __str__(self):
        
        # empty Polynomial (constant 0) dealt with
        if len(self.data) == 0:
            return '0'
        
        string = ''
        
        if self.data[0] != 0:
            string += str(self.data[0])
        if self.data[1] == 1:
            string += '+' + 'X'
        elif self.data[1] > 0:
            string += '+' + str(self.data[1]) + '*X'
        elif self.data[1] == -1:
            string += '-' + 'X'
        elif self.data[1] < 0:
            string += str(self.data[1]) + '*X'
        n = 1
        for i in self.data[2:]:
            n += 1
            if i == 1:
                string += '+' + 'X' + '**' + str(n)
            elif i > 0:
                string += '+' + str(i) + '*X' + '**' + str(n)
            elif i == -1:
                string += '-' + 'X' + '**' + str(n)
            elif i < 0:
                string += str(i) + '*X' + '**' + str(n)
        if string[0] == '+':
            return string[1:]
        return string

                    
    
    def __repr__(self):
        return "Polynomial(" + str(self.data) + ")"
    
    def __iadd__(self, other):
        ml = min(len(self.data), len(other.data))
        for i in range(ml):
            self.data[i] += other.data[i]
        if len(other.data) > len(self.data):
            self.__data += other.data[ml:]
        self.__truncate()
        return self
    
    def __add__(self, other):
        if type(other) is not Polynomial:
            other = Polynomial([other])
        ans = self.copy()
        ans += other
        return ans
    
    def __radd__(self, other):
        return self + other
        
    def __isub__(self, other):
        ml = min(len(self.data), len(other.data))
        for i in range(ml):
            self.data[i] -= other.data[i]
        if len(other.data) > len(self.data):
            self.data += [-x for x in other.data[ml:]]
        self.__truncate()
        return self
            
    def __sub__(self, other):
        if type(other) is not Polynomial:
            other = Polynomial([other])
        ans = self.copy()
        ans -= other
        return ans
    
    def __rsub__(self, other):
        return -self + other
        
    def __imul__(self, other):
        newdata = [0 for i in range(len(self.data) + len(other.data) - 1)]
        for i in range(len(newdata)):
            lb = max(0, i - len(other.data) + 1)
            ub = min(len(self.data) - 1, i)
            for j in range(lb, ub + 1):
                newdata[i] += self.data[j] * other.data[i-j]
        self.__data = newdata
        self.__truncate()
        return self

    
    def __mul__(self, other):
        if type(other) is not Polynomial:
            other = Polynomial([other])
        ans = self.copy()
        ans *= other
        return ans
    
    def __rmul__(self, other):
        return self * other
    
    def __neg__(self):
        ans = self.copy()
        ans.__data = [-x for x in ans.data]
        return ans
    
    def __pow__(self, n):
        ans = Polynomial([1])
        for i in range(n):
            ans = ans * self
        return ans
    
    def __call__(self, value):
        currentpower = 1
        ans = 0
        for i in self.data:
            ans += i * currentpower
            currentpower *= value
        return ans
    
    def __truncate(self):
        if len(self.data) > 0:
            if self.data[-1] == 0:
                if len(self.data) == 1:
                    self.__data = []
                    return 
                else:
                    for i in range(2, len(self.data) + 1):
                        if self.data[-i] != 0 and self.data[-i+1] == 0:
                            del self.__data[-i+1:]
                            return
                        if i == len(self.data):
                            self.__data = []
                            return
                        
    
    def copy(self):
        return Polynomial(self.data[:])
    
    def __eq__(self, other):
        self.__truncate()
        other.__truncate()
        return self.data == other.data
    
    def primitive(self):
        data = self.data[:]
        for i in range(len(self.data)):
            data[i] *= 1/ (1+i)
        return Polynomial([0] + data)
    
    def integrate(self, a, b):
        return self.primitive()(b) - self.primitive()(a)
        
    
x = Polynomial([0,1])
    
            