import numpy as np
import random as rnd
import sys
import scipy.optimize

# dictionary = {'c_k': [alpha_k, c_k]}


################################# FUNCTIONS ##################################

def c_k(dictionary):
    c_k_list = [dictionary[key][1] for key in dictionary.keys()]
    return np.array(c_k_list)

def alpha_k(dictionary):
    alpha_k_list = [dictionary[key][0] for key in dictionary.keys()]
    return np.array(alpha_k_list)

def f(x, d):
    value = 0
    for key in d.keys():
        alpha = d[key][0]
        c = d[key][1]
        value += alpha*scipy.exp(c*x)
    return value

################################### INPUT ####################################


# observable = np.array([rnd.randint(0,1) for _ in range(N)])


#################################### HMM #####################################

def forwardprop(obs, mu, rho, n):
    N = len(obs)
    lam = 1/n
    coef_list = []
    
# zeroth iteration (first)
    coef_0 = dict()
    if obs[0] == 0:
        z_0 = lam / (lam + 2 * mu)
        
        alpha = lam / z_0
        c = - lam - 2 * mu
        key = str(round(c, 4))
        coef_0[key] = [alpha, c]
    else:
        z_0 = 2 * mu / (lam + 2 * mu)
        
        alpha = lam / z_0
        c = - lam
        key = str(round(c, 4))
        coef_0[key] = [alpha, c]
        
        alpha = -lam / z_0 
        c = - lam - 2 * mu
        key = str(round(c, 4))
        coef_0[key] = [alpha, c]
    coef_list.append(coef_0)

    for k in range(1, N):
        D = coef_list[k - 1]     # previous dictionary
        coef_k = dict()        # current dictionary
        A_K = alpha_k(D)
        C_K = c_k(D)
        if obs[k - 1] == 0:
            z_i = sum(A_K * (2 * rho * lam / 
                             ((lam + 2 * mu) * C_K * (C_K - 2 * rho)) - 
                             1 / (C_K - 2 * rho - 2 * mu)))
            alpha = lam / z_i * sum(A_K * (1/(C_K-2*rho) - 1/(C_K)))
            c = -lam - 2 * mu
            key = str(round(c, 4))
            coef_k[key] = [alpha, c]
            for i in range(len(D)):
                alpha_new = A_K[i]/z_i
                c = C_K[i] - 2*rho - 2*mu
                key = str(round(c, 4))
                if key in coef_k.keys():
                    coef_k[key][0] += alpha_new
                else:
                    coef_k[key] = [alpha_new, c]
        else:
            z_i = sum(A_K*((1/C_K+1/(C_K-2*mu)) * (2 * mu / (lam + 2 * mu)) - 
                           1 / (C_K - 2 * rho) + 1 / (C_K - 2 * rho - 2 * mu)))
            c = - lam
            alpha = lam / z_i * sum(A_K * (1/(C_K - 2 * rho) - 1/C_K))
            key = str(round(c, 4))
            coef_k[key] = [alpha, c]
            
            c = - lam - 2 * mu
            alpha = - alpha
            key = str(round(c, 4))
            coef_k[key] = [alpha, c]
            for i in range(len(D)):
                alpha_new = A_K[i]/z_i
                c_1 = C_K[i] - 2 * rho
                key_1 = str(round(c_1, 4))

                c_2 = C_K[i] - 2*rho - 2*mu
                key_2 = str(round(c_2, 4))
                if key_1 in coef_k.keys():
                    coef_k[key_1][0] += alpha_new
                else:
                    coef_k[key_1] = [alpha_new, c_1]
                if key_2 in coef_k.keys():
                    coef_k[key_2][0] += - alpha_new
                else:
                    coef_k[key_2] = [- alpha_new, c_2]
        coef_list.append(coef_k)
    return coef_list


def backwardprop(ceof_list, obs, mu, rho, n):
    N = len(obs)
    lam = 1/n
    height_list = [0 for _ in range(N)]
    argmax_n = scipy.optimize.fmin(lambda x: -f(x, ceof_list[-1]), 0)[0]
    if argmax_n < 0:
        print(0)
    height_list[-1] = argmax_n
    for i in range(2, N + 1):
        t_prev = height_list[-i+1]
        if obs[-i] == 0:
            p_eq = ((1 - np.exp(-2 * rho * t_prev)) * lam * np.exp(-lam*t_prev) 
                    + np.exp(-2 * rho * t_prev)) * np.exp(-2 * mu * t_prev)
            p_ineq = (1 - np.exp(-2 * rho * t_prev)) * lam
            if p_eq > p_ineq:
                t_i = t_prev
            else:
                t_i = 0
            if t_i < 0:
                print(i, 1)
            height_list[-i] = t_i
        elif obs[-i] == 1:
            p_eq = ((1 - np.exp(-2 * rho * t_prev)) * lam * np.exp(-lam*t_prev) 
                    + np.exp(-2 * rho * t_prev)) * (1 - np.exp(-2 * mu * t_prev))
            p_ineq = ((1 - np.exp(-2 * rho * t_prev)) * 2 * mu * lam / (2 * mu + lam) + 
                      (lam / (2 * mu + lam))**(lam / (2 * mu)))
            if p_eq > p_ineq:
                t_i = t_prev
            else:
                t_i = - np.log(lam / (2 * mu + lam)) / (2 * mu)
            if t_i < 0:
                print(i, 2)
            height_list[-i] = t_i
    return height_list


def backwardprop2(coef_list, obs, mu, rho, n):
    N = len(obs)
    height_list = [scipy.optimize.fmin(lambda x: -f(x, coef), 0)[0] for coef in coef_list]
    return height_list