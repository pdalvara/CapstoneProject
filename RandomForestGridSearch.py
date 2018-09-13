from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import sklearn.tree as tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
%matplotlib inline
plt.style.use("ggplot")

#Create model
clf = RandomForestClassifier(n_jobs=-1, criterion='entropy')

#Create paramaters
param_grid = {
    'n_estimators': [10, 20, 30, 50, 100],
    'max_depth': [None, 5, 10, 15],
    'max_features': ['auto', 3, 5, 10],
    'criterion': ['entropy', 'gini']

}

scorers = {
    'precision_score': make_scorer(precision_score),
    'recall_score': make_scorer(recall_score),
    'accuracy_score': make_scorer(accuracy_score)
}

def grid_search_wrapper(refit_score='precision_score'):
    """
    fits a GridSearchCV classifier using refit_score for optimization
    prints classifier performance metrics
    """
    grid_search = GridSearchCV(clf, param_grid, scoring=scorers, refit=refit_score,
                           return_train_score=True, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    y_pred = grid_search.predict(X_test)

    print('Best params for {}'.format(refit_score))
    print(grid_search.best_params_)

    # confusion matrix on the test data.
    print('\nConfusion matrix of Random Forest optimized for {} on the test data:'.format(refit_score))
    print(pd.DataFrame(confusion_matrix(y_test, y_pred),
                 columns=['pred_neg', 'pred_pos'], index=['neg', 'pos']))
    return grid_search

#Puts results in a table for clear view of outcomes of each model
results = pd.DataFrame(grid_search_clf.cv_results_)
results = results.sort_values(by='mean_test_recall_score', ascending=False)
results[['mean_test_precision_score', 'mean_test_recall_score', 'mean_test_accuracy_score', 'param_max_depth',
        'param_max_features', 'param_n_estimators']].round(3).head()
