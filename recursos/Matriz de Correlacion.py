print(dta.corr())


    correlacion = df_abandonos.corr() 
    fig, ax = plt.subplots(figsize=(21, 21)) 
    ax.matshow(correlacion) 
    plt.xticks(range(len(correlacion.columns)), correlacion.columns); 
    plt.yticks(range(len(correlacion.columns)), correlacion.columns); 