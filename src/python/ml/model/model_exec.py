from tabulate import tabulate
from sklearn.metrics import recall_score,f1_score,precision_score,accuracy_score, make_scorer
from sklearn.model_selection import KFold,cross_validate

import time

def get_predict_from_model(model,x_test):
    y_pred = model.predict(x_test)
    return y_pred

# Run model and get accuracy
def get_accuracy_score(model,x_test,y_test,model_name):
    y_pred = get_predict_from_model(model,x_test)
    acc_score = accuracy_score(y_test, y_pred)
    # poly_f1 = f1_score(y_test, poly_pred, average='weighted')
    # print('Accuracy (RBF Kernel): ', "%.2f" % (rbf_accuracy*100))
    # cm = confusion_matrix(y_test, y_pred)
    acc_score = "{0:.0%}".format(acc_score)
    print('Model: {model_name} \nUsing: Train/Test Split \nAccuracy: {acc_score}\n'.format(model_name=model_name,acc_score=acc_score))
    return y_pred

def run_model(model,x_train, y_train,x_test,y_test,model_name):
  start = time.time()
  model.fit(x_train, y_train)
  stop = time.time()
  time_mins = (stop-start) // 60
  time_secs = (stop-start) % 60
  print(f"Training time: {round(time_mins)} mins {round(time_secs)} sec")
  return get_accuracy_score(model,x_test,y_test,model_name)


# Run model with cross validation and get accuracy, precision, recall, F1 scores

def run_model_with_cv(model_name,model, x, y,n_splits=5):
    start = time.time()
    kf=KFold(n_splits=n_splits)
    scoring = {'accuracy': 'accuracy',
               'f1': make_scorer(f1_score, zero_division=1, average='weighted'),
               'precision': make_scorer(precision_score, zero_division=1, average='weighted'),
               'recall': make_scorer(recall_score, zero_division=1, average='weighted')}
    results = cross_validate(estimator=model,
                              X=x,
                              y=y,
                              cv=kf,
                              scoring=scoring,
                              return_train_score=True)
    data = [["Accuracy",
             "{0:.0%}".format(results['train_accuracy'].mean()),
             "{0:.0%}".format(results['test_accuracy'].mean())],
            ["Precision",
             "{0:.0%}".format(results['train_precision'].mean()),
             "{0:.0%}".format(results['test_precision'].mean())],
            ["Recall",
             "{0:.0%}".format(results['train_recall'].mean()),
             "{0:.0%}".format(results['test_recall'].mean())],
            ["F1",
             "{0:.0%}".format(results['train_f1'].mean()),
             "{0:.0%}".format(results['test_f1'].mean())]]
    stop = time.time()
    time_mins = (stop-start) // 60
    time_secs = (stop-start) % 60
    print(f"CV Training time: {round(time_mins)} mins {round(time_secs)} sec")
    print("Model: ", model_name)
    print("Using: ",n_splits,"-fold cross validation")
    print(tabulate(data, headers=["Score", "Training", "Validation"]))
    return results