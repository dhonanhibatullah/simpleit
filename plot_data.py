import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

DATA_NUMBER = 0

def main():
    df  = pd.read_csv(f'data/{DATA_NUMBER:05d}.csv')
    vin = df['vin'].to_numpy()
    vd  = df['vd'].to_numpy()
    t   = np.arange(0, len(vin), 1) 

    plt.plot(t, vin)
    plt.plot(t, vd)
    plt.show()

if __name__ == '__main__':
    main()