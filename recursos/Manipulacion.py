#dta.drop(['age','yrs_married'],axis=1,inplace=True)
#dta.head()

#Creamos una nueva variable binaria "infidelidad" para tratarlo como un problema de clasificación 0=fiel, 1=infiel
#Mostramos los primeros....infieles
dta['infidelidad']=(dta.affairs>0).astype(int)