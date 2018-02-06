import scipy

class SumOfExp:
    def __init__(self, coef_dict):
        self.__coef_dict = coef_dict

    @property
    def coef_dict(self):
        return self.__coef_dict
    
    def copy(self):
        return SumOfExp(self.coef_dict.copy())
    
    def keys(self):
        return self.coef_dict.keys()
    
    def __getitem__(self, key):
        return self.coef_dict[key]

    def __iadd__(self, sumexp):
        new_dict = self.coef_dict.copy()
        for key in sumexp.keys():
            if key in new_dict.keys():
                new_dict[key][0] += sumexp[key][0]
            else:
                new_dict[key] = sumexp[key]
        return SumOfExp(new_dict)
    
    def __add__(self, other):
        ans = self.copy()
        ans += other
        return ans
    
    def __radd__(self, other):
        return self + other

    def __imul__(self, other): 
        """
        scalar and sumexp
        """
        if type(other) is float or type(other) is int:
            new_dict = dict()
            for key in self.keys():
                new_dict[key] = [self[key][0] * other, self[key][1]]
            return SumOfExp(new_dict)
        if type(other) is SumOfExp:
            new_sum = SumOfExp(dict())
            for key in other.keys():
                new_dict = dict()
                two_list = other[key]
                for key in self.keys():
                    a_k = self[key][0] * two_list[0]
                    c_k = self[key][1] + two_list[1]
                    new_key = str(round(c_k, 4))
                    new_dict[new_key] = [a_k, c_k]
                new_sum += SumOfExp(new_dict)
            return new_sum

    def __mul__(self, other):
        ans = self.copy()
        ans *= other
        return ans
    
    def __rmul__(self, other):
        return self * other
    
    def __itruediv__(self, other):
        if type(other) is int or type(other) is float:
            new_dict = dict()
            for key in self.keys():
                new_dict[key] = [self[key][0] / other, self[key][1]]
            return SumOfExp(new_dict)
        
    def __truediv__(self, other):
        if type(other) is int or type(other) is float:
            ans = self.copy()
            ans /= other
            return ans

    def integrate(self):
        ans = 0.
        for key in self.keys():
            if self[key][1] >= 0:
                return 'Infinity'
            ans -= self[key][0] / self[key][1]
        return ans
    
    def __repr__(self):
        return ''.join(['SumOfExp(', str(self.coef_dict), ')'])
    
    def __str__(self):
        string_list = []
        for key in self.keys():
            if self[key][1] == 0:
                string = str(round(self[key][0], 4)) + '+'
            else:
                string = str(round(self[key][0], 4)) + ' Exp[' + str(round(self[key][1], 4)) + 't' + ']' + '+'
            string_list.append(string)
        string_list[-1] = string_list[-1][:-1]
        return ''.join(string_list)
    
    def __eq__(self, other):
        return self.coef_dict == other.coef_dict
    
    def f(self, x):
        value = 0
        for key in self.keys():
            alpha = self[key][0]
            c = self[key][0]
            value += alpha*scipy.exp(c*x)
        return value
    
    def maximize(self):
        val = scipy.optimize.fmin(lambda x: -self.f(x), 0)[0]
        return val