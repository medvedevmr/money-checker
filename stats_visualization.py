import pandas as pd
import circlify
import matplotlib.pyplot as plt
import microservices

def stats_pic():
    date = microservices.get_date()

    df2 = pd.read_csv('payment_history.csv')

    options = ['Paid'] 
            
    # selecting rows based on condition 
    rslt_df = df2[df2['Action'].isin(options)]

    df_grouped = rslt_df.groupby('Category')['Sum USD']
    group_keys = df_grouped.groups.keys()

    df_grouped_sum = df_grouped.sum()
    group_vals = [x for x in df_grouped_sum]
    group_sum = sum(group_vals)
    #print(df_grouped,df_grouped.groups.keys())

    # compute circle positions:
    circles = circlify.circlify(
        group_vals, 
        show_enclosure=False, 
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )

    # Create just a figure and only one subplot
    fig, ax = plt.subplots(figsize=(10,10))

    # Title
    ax.set_title('Spend Statistic by category')

    # Remove axes
    ax.axis('off')

    # Find axis boundaries
    lim = max(
        max(
            abs(circle.x) + circle.r,
            abs(circle.y) + circle.r,
        )
        for circle in circles
    )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    
    colors = ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a", "#ffee65"]
    # print circles
    for circle, label, val, color in zip(circles, group_keys, group_vals, colors):
        x, y, r = circle
        ax.add_patch(plt.Circle((x, y), r, alpha=0.2, linewidth=2,facecolor=color))
        plt.annotate(
            label,
            (x,y+0.03 ) ,
            va='center',
            ha='center'
        )
        plt.annotate(
            val,
            (x,y-0.01 ) ,
            va='center',
            ha='center'
        )
        plt.annotate(
            str(round((val/group_sum)*100,2))+'%',
            (x,y-0.05 ) ,
            va='center',
            ha='center'
        )
    file_name = 'temp_pics/{}-{}-{}.png'.format(date[0],date[1],date[2])
    plt.savefig(file_name)
    return file_name
stats_pic()