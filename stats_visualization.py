import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import microservices

def stats_pic():
    date = microservices.get_date()

    df = pd.read_csv('payment_history.csv')

    options = ['Paid'] 
        
    # selecting rows based on condition 
    rslt_df = df[df['Action'].isin(options)]

    df_grouped = rslt_df.groupby('Category')['Sum USD'].sum()
    
    df_plot = df_grouped.plot.barh(figsize=(10,8))
    
    df_plot.bar_label(df_plot.containers[0])
    
    file_name = 'temp_pics/{}-{}-{}.png'.format(date[0],date[1],date[2])
    plt.savefig(file_name)
    return file_name