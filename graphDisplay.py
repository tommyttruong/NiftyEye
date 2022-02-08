import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use('fivethirtyeight')
fig = plt.figure()
#ax = fig.add_axes([0,0,1,1])

def animate():
    df = pd.read_csv('real time nft sales.csv')
    ys = df['Name'].tolist()
    xs = df['tenMinute'].tolist()
    
    plt.cla()
    
    plt.bar(ys, xs)
    
ani = FuncAnimation(fig, animate(), interval=1000)
plt.show()
    
    