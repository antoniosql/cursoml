import matplotlib.pyplot as plt

# Creamos el fit lineal utilizando el conjunto de entrenamiento
plt.scatter(X_train, y_train, color = 'red')
plt.plot(X_train, lr.predict(X_train), color = 'blue')

plt.show()