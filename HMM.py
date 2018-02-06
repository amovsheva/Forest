import numpy as np
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##############################################################################
############################ HIDDEN MARKOV MODEL #############################
##############################################################################

################################# CONSTANTS ##################################

# chain length
length = 100
# stochastic matrix
# probability of staying in place: 0.5
# probability of moving left: 0.25
# probability of moving right: 0.25
# P = P(x_k+1 | x_k), 
n = 10
P = np.zeros((n,n), dtype = float)
for i in range(n - 1):
    P[i, i + 1] = 0.25
    P[i + 1, i] = 0.25
    P[i, i] = 0.5
P[0, -1] = 0.25
P[-1, 0] = 0.25
P[-1, -1] = 0.5


# K = P(y_k| x_k), where y_k is observable, and x_k is the hidden variable
k = 10
K = np.zeros((n, k), dtype = float)
for i in range(n):
    for j in range(i-2, i+3):
        K[i,j%k] = rnd.random()
    K[i, :] = K[i,:]/sum(K[i, :])
    
    
################################# FUNCTIONS ##################################


def hidden_variables(length, P_matrix):
    """
    Creating Markov Chain
    """
    n = len(P_matrix)
    chain = np.zeros(length, dtype = int)
    x_i = 0
    chain[0] = x_i
    for i in range(1, length):
        x_i = np.random.choice(np.arange(0, n), p = P_matrix[chain[i-1], :])
        chain[i] = x_i
    return chain


def observable_variables(hidden_chain, K_matrix):
    """
    Creating observables for the Markov Chain
    """
    length = len(hidden_chain)
    y = np.zeros(length, dtype = int)
    k = len(K_matrix[0])
    for i in range(length):
        y_i = np.random.choice(np.arange(0, k), p = K_matrix[hidden_chain[i], :])
        y[i] = y_i
    return y

def HMM(observables, P_matrix, K_matrix):
    """
    Given observables we find most likely chain of hidden variables
    """
    length = len(observables)
    n = len(P_matrix)
    k = len(K_matrix[0])
    prior = np.ones(n, dtype = float)/n
    for y in observables:
        Pxy = prior * K_matrix[:, y] / np.dot(prior, K_matrix[:, y])
        prior = np.dot(Pxy, P_matrix)

    probable_chain = 11*np.ones(length, dtype = int)
    probable_chain[-1] = np.argmax(Pxy)
    for i in range(2, length + 1):
        probable_chain[-i] = np.argmax(P_matrix[:, probable_chain[-i+1]] * K_matrix[:, observables[-i]])
    return probable_chain
    

    
##############################################################################
####################### CONTINUOUS HIDDEN MARKOV MODEL #######################
##############################################################################

s_gps = 0.01
s_m = 0.3


def continuous_hidden_variables(length, sigma_m):
    """
    Creating Markov Chain
    """
    chain = np.zeros(length, dtype = float)
    x_i = 0
    chain[0] = x_i
    for i in range(1, length):
        x_i = np.random.normal(chain[i-1], np.sqrt(sigma_m))
        chain[i] = x_i
    return chain

def continuous_observable_variables(hidden_chain, sigma_gps):
    """
    Creating observables for the Markov Chain
    """
    length = len(hidden_chain)
    y = np.zeros(length, dtype = float)
    for i in range(length):
        y_i = np.random.normal(hidden_chain[i], np.sqrt(sigma_gps))
        y[i] = y_i
    return y


def CHMM(observables, sigma_m, sigma_gps):
    """
    Given observables we find most likely chain of hidden variables
    """
    length = len(observables)
    sigma_i = observables[0]
    center_i = sigma_gps
    for y in observables[1:]:
        ### prior
        center_i = center_i
        sigma_i = sigma_i + sigma_m
        ### conditional prob
        center_i = (y*sigma_i + center_i * sigma_gps)/(sigma_i + sigma_gps)
        sigma_i = sigma_i * sigma_gps / (sigma_i + sigma_gps)
        #print(sigma_i)
    # sigma_n = -sigma_m + np.sqrt(sigma_m*(sigma_m+4sigma_gps))
    probable_chain = np.ones(length, dtype = float)
    probable_chain[-1] = center_i
    for i in range(2, length + 1):
        probable_chain[-i] = (probable_chain[-i + 1]*sigma_gps + 
                              observables[-i]*sigma_m) / (sigma_gps+sigma_m)
    return probable_chain


def error(sigma_m, sigma_gps):
    if type(sigma_m) is float and type(sigma_gps) is list:
        L = len(sigma_gps)
        ERROR = []
        for i in range(L):
            CHV = continuous_hidden_variables(1000, sigma_m)
            COV = continuous_observable_variables(CHV, sigma_gps[i])
            PHV = CHMM(COV, sigma_m, sigma_gps[i])
            ERROR_i = [(x)**2 for x in PHV-CHV]
            ERROR.append(np.mean(ERROR_i))
        return ERROR
    else:
        CHV = continuous_hidden_variables(1000, sigma_m)
        COV = continuous_observable_variables(CHV, sigma_gps)
        PHV = CHMM(COV, sigma_m, sigma_gps)
        ERROR_i = [(x)**2 for x in PHV-CHV]
        return np.mean(ERROR_i)
    
    
def PlotGraphs(sigma_m, sigma_gps_range):
    error_list = [error(s_m,x) for x in sigma_gps_range]
    
    plt.figure()
    plt.plot(sigma_gps_range, error_list, 'b')
    plt.xlabel('Error')
    plt.ylabel('$\sigma_gps$')
    plt.title('$\sigma_m$ = %f' % (sigma_m))
    plt.show()
