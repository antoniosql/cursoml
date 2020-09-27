#binary features
import pandas as pd 
from sklearn.preprocessing import StandardScaler

customers = pd.read_csv('../datos/Telco-Customer-Churn.csv')


customers['TotalCharges'] = pd.to_numeric(customers['TotalCharges'],errors='coerce')
customers['MonthlyCharges'] = pd.to_numeric(customers['MonthlyCharges'],errors='coerce')
customers.dropna(axis=0,inplace=True)


binary_features = ['PhoneService',
                  'Dependents',
                  'Partner',
                  'PaperlessBilling',
                  'Churn']
for feat in binary_features:
    customers[feat] = customers[feat].astype('category').cat.codes

from sklearn.preprocessing import  LabelEncoder
le=LabelEncoder()
customers['gender'] = le.fit_transform(customers['gender'])


#dummy features
dummy_features = ['PaymentMethod',
                 'Contract',
                 'StreamingMovies',
                 'TechSupport',
                 'DeviceProtection', 
                 'OnlineBackup',
                 'OnlineSecurity',
                 'InternetService',
                 'MultipleLines',
                 'StreamingTV']

dummies = pd.get_dummies(customers, columns = dummy_features)
customers = pd.merge(customers, dummies)
customers.drop(columns = dummy_features, inplace = True)

#customers.dropna(axis=0,inplace=True)
#for col in customers.columns:
 #   print(col)

#customers['TotalCharges'] = customers['TotalCharges'].astype(float)


#Scale the non-binary, not dummy values
not_binary_values = ['tenure', 'TotalCharges']

scaler = StandardScaler()

customers[not_binary_values] = scaler.fit_transform(customers[not_binary_values])

#Final scaled, transformed X for modeling
scaled_X = customers.drop(columns = ['customerID'])



#Kmeans
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

kmeans = KMeans(n_clusters=5)
kmeans.fit(scaled_X)

scores = [KMeans(n_clusters=i+2).fit(scaled_X).inertia_ for i in range(20)]
sns.lineplot(np.arange(2, 22), scores)
plt.xlabel('Number of clusters')
plt.ylabel("Inertia")
plt.title("Inertia of KMeans versus number of clusters")

#Evaluación
from sklearn.metrics import silhouette_score,davies_bouldin_score
#silhouette scores
print('kmeans: {}'.format(silhouette_score(scaled_X, kmeans.labels_, metric='euclidean')))
#db index
print('kmeans: {}'.format(davies_bouldin_score(scaled_X, kmeans.labels_)))


scaled_X['cluster'] = kmeans.labels_
#Usamos RandomForest para interpretar

from sklearn.ensemble import RandomForestClassifier

#take the noise out of the model
scaled_X_no_noise = scaled_X[scaled_X.cluster != -1].copy()
scaled_X_no_noise.drop(columns = ['TotalCharges', 'MonthlyCharges'], inplace = True)

#build the RFC classifier to calculate MDI as a proxy for feature importance
y = scaled_X_no_noise.iloc[:,-1]
X = scaled_X_no_noise.iloc[:,:-1]
clf = RandomForestClassifier(n_estimators=100).fit(X, y)
selected_columns = list(pd.DataFrame(np.array([clf.feature_importances_, X.columns]).T, columns=['Importance', 'Feature'])
           .sort_values("Importance", ascending=False)
           .head(10)
           .Feature
           .values)

# melt the data against the cluster
top_features = scaled_X_no_noise[selected_columns+['cluster']].melt(id_vars='cluster')

#plot the data
fig, ax = plt.subplots(figsize=(20, 8))
sns.barplot(x='cluster', y='value', hue='variable', data=top_features, palette='Set3')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
          ncol=3, fancybox=True, shadow=True)
plt.ylabel('Gini Index')
plt.xlabel('KMeans Cluster')
#plt.savefig('randomforest.png', dpi=300)
plt.show