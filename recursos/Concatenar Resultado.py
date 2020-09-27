predict=kmeans.predict(df_normalized)


df['Cluster'] = pd.Series(predict, index=df.index)