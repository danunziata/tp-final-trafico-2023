import matplotlib.pyplot as plt

def grafica(l, s):
    
    plt.plot(l, s)
    
    plt.xlabel('Tasa de arribo [lamda]')
    plt.ylabel('tiempo [segundos]')
    
    plt.title('Tiempo medio del sistema')
    
    plt.legend()
    
    plt.show()

l= [1, 2, 3, 4, 5]
s = [10, 20, 15, 25, 30]
grafica(l, s)
