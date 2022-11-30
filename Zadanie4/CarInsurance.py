import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeRegressor, export_graphviz

pf = pd.read_csv("data/data.csv")

df = pf.to_numpy()

print(df)

X = df[:, 0:1].astype(int)
y = df[:, 1].astype(float)

print(X)
print(y)

regressor = DecisionTreeRegressor(random_state=0)

regressor.fit(X, y)

y_pred = regressor.predict([[61]])

print(y_pred)

# arange for creating a range of values
# from min value of X to max value of X
# with a difference of 0.01 between two
# consecutive values
X_grid = np.arange(min(X), max(X), 0.1)

# reshape for reshaping the data into
# a len(X_grid)*1 array, i.e. to make
# a column out of the X_grid values
X_grid = X_grid.reshape((len(X_grid), 1))

# scatter plot for original data
plt.scatter(X, y, color='red')

# plot predicted data
plt.plot(X_grid, regressor.predict(X_grid), color='blue')

# specify title
plt.title('Claims to Total payment (Decision Tree Regression)')

# specify X axis label
plt.xlabel('Number of claims')

# specify Y axis label
plt.ylabel('Total payment for claims')

# show the plot
plt.show()

export_graphviz(regressor, out_file='tree.dot', feature_names=['Claims'])
