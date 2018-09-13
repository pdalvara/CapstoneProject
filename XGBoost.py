from xgboost import XGBClassifier
import xgboost as xgb
from xgboost import plot_tree
from sklearn.metrics import confusion_matrix

#Create Model
xg_model = XGBClassifier(learning_rate=.1, n_estimators=1000,
                         max_depth=5, subsample=.8, colsample_bytree=.8,
                        random_state=0)

#Pass in X and y variables to fit model
xg_model.fit(X, y)

#Make predictions with model
y_pred = xg_model.predict(X_test)

#Use confusion matrix to evaluate performance of model
confusion_matrix(y_test, y_pred)

#Graph Feature importances
importances = list(zip(xg_model.feature_importances_, X_test.columns))
importances.sort(reverse=True)
pd.DataFrame(importances, index=[x for (_,x) in importances]).plot(kind = 'bar')

#Plot an XGBoost Tree that shows how decisions were made
plot_tree(xg_model)
fig = plt.gcf()
fig.set_size_inches(150, 100)
