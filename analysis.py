#/usr/bin/env python

import pandas as pd
from sklearn import model_selection
from sklearn import metrics
from sklearn import linear_model
from sklearn import svm

#names = ['Congress', 'Bill_ID', 'Bill_Type', 'Num_cosponsors','Committee', 'Subject' ,'Status']
congressData = pd.read_csv('congress_data.csv', sep = ',')

# Only take H.R., S., H.J.Res, S.J.Res bills.
billsData = congressData[(congressData['Bill_Type']=='hr') | (congressData['Bill_Type']=='s') | (congressData['Bill_Type']=='hjres') | (congressData['Bill_Type']=='sjres')]

# Only house and senate Judiciary committee
judiciaryData = billsData[(billsData['Committee']=='Senate Judiciary') | (billsData['Committee']=='House Judiciary')]

# Immigration topics from Judiciary committees
immigrationData = judiciaryData[judiciaryData['Major_subject']=='Immigration']
immigrationData = immigrationData.replace({'House Judiciary': 0, 'Senate Judiciary': 1, 'hr': 0, 's':1, 'hjres':2, 'sjres':3})



data = immigrationData.values

#data = judiciaryData.values
X_feat   = data[:, [0,2,5,6,7]]
Y_target = data[:, 9]

# Splitting the data set to train and validation subsets
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X_feat, Y_target, test_size=0.25, random_state=7)

# Applying LR model
lr = linear_model.LogisticRegression(penalty='l2', dual=False, tol=0.000001, C=10.0,
                        fit_intercept=True, intercept_scaling=1,
                        class_weight=None, random_state=1, solver='newton-cg',
                        max_iter=1000, multi_class='multinomial', verbose=0,
                        warm_start=False, n_jobs=4)
# Fitting the model
lr.fit(X_train, Y_train)

# Applying SVC
clf = svm.SVC(kernel="poly", gamma='scale', decision_function_shape='ovo')
clf.fit(X_train, Y_train)

print "Logistic Regression method:"
predictions = lr.predict(X_validation)
print(metrics.accuracy_score(Y_validation, predictions))
print(metrics.confusion_matrix(Y_validation, predictions))
print(metrics.classification_report(Y_validation, predictions))

print "Support Machine Vectors method:"
predictions = clf.predict(X_validation)
print(metrics.accuracy_score(Y_validation, predictions))
print(metrics.confusion_matrix(Y_validation, predictions))
print(metrics.classification_report(Y_validation, predictions))
