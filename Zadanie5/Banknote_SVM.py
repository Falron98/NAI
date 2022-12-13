import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

columns = ["Variance", "Skewness", "Curtosis", "Entropy", "Class"]
banknote = pd.read_csv('data/data_banknote_authentication.txt', names=columns)

print(banknote.head(5))

sns.pairplot(banknote, hue='Class')

plt.show()

x, y = banknote.drop('Class', axis=1), banknote['Class']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

print("x train shape ", x_train.shape)
print("x test shape ", x_test.shape)

linear_svc_classifier = SVC(kernel="linear")
linear_svc_classifier.fit(x_train, y_train)

linear_svc_classifier_prediction = linear_svc_classifier.predict(x_test)

print(confusion_matrix(y_test, linear_svc_classifier_prediction))

print(classification_report(y_test, linear_svc_classifier_prediction))

print("accuracy of linear svm", accuracy_score(y_test, linear_svc_classifier_prediction) * 100, "%")
