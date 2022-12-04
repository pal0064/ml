from sklearn.naive_bayes import MultinomialNB,GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

# Functions to load each model

def get_gaussian_model(model_name):
  models = {
      'GaussianNB':GaussianNB,
      'MultinomialNB':MultinomialNB

  }
  model = models[model_name]()  
  return model

def get_random_forest_model(n_estimators=100):
  model = RandomForestClassifier(n_estimators=n_estimators)
  return model

def get_knn_model(n_neighbors=5,metric='minkowski',p=2): # p is power parameter,Euclidean Distance
    model = KNeighborsClassifier(n_neighbors = n_neighbors, metric =metric, p = p)
    return model

def get_svm_model(poly_degree=3,poly_c=1):
  model = svm.SVC(kernel='poly', degree=poly_degree, C=poly_c)
  return model
