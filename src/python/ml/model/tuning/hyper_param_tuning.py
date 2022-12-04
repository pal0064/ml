from sklearn import svm
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
from skopt.plots import plot_objective, plot_histogram



def tune_hyperparam_for_model(model,param_grid,n_iter,cv,x_train,y_train,random_state=0):
  tuned_model = BayesSearchCV(
      model,
      param_grid,
      n_iter=n_iter,
      random_state=random_state,
      cv=cv
  )
  tuned_model.fit(x_train, y_train)
  return tuned_model


def tune_svm_model(x_train,y_train,param_grid= {
            'C': Real(1e-6, 1e+6, prior='log-uniform'),
            'gamma': Real(1e-6, 1e+1, prior='log-uniform'),
            'degree': Integer(1,8),
            'kernel': Categorical(['linear', 'poly', 'rbf','sigmoid']),
        }, n_iter=10,cv = 3 ):

    model = svm.SVC()
    # tuning using bayesian optimization
    final_model = tune_hyperparam_for_model(model,param_grid,n_iter,cv,x_train, y_train)
    return final_model



def show_tuned_model_performance(final_model,x_test,y_test):
    print("test score: %s" % final_model.score(x_test, y_test))
    print("val. score: %s" % final_model.best_score_)
    print("best params: %s" % str(final_model.best_params_))