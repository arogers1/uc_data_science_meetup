from __future__ import division
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import export_graphviz
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from IPython.display import Image
import StringIO, pydot
%matplotlib 

dental_df = pd.read_csv("dental_data.csv")
cols = [c for c in dental_df.columns if c not in ("patient_id","patient_id.1","name","responsible_party","birth_year","prim_employer_id","sec_employer_id","first_visit_date","last_date_seen","date_entered","next_regular_appointment","next_preventive_appointment","next_recall_date","is_active","zipcode","city")
]
dental_df["city"] = pd.factorize(dental_df["city"])[0]
dental_df["state"] = pd.factorize(dental_df["state"])[0]
dental_df["marital_status"] = pd.factorize(dental_df["marital_status"])[0]
dental_df["policy_holder_status"] = pd.factorize(dental_df["policy_holder_status"])[0]
dental_df["patient_status"] = pd.factorize(dental_df["patient_status"])[0]
dtree = DecisionTreeClassifier(criterion="entropy",max_depth=4)
X = dental_df[cols].values
y = dental_df["is_active"].values

Xr, Xt, yr, yt = train_test_split(X, y, train_size=4000, test_size=1797, random_state=42)
dtree.fit(Xr, yr)
ypred = dtree.predict(Xt)
dtree.fit(Xr, yr)

dot_data = StringIO.StringIO()
export_graphviz(dtree, out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_png("dental_tree_ent.png")

print (confusion_matrix(yt, ypred), accuracy_score(yt, ypred))
pd.crosstab(yt, ypred, rownames=['actual'],colnames=['prediction'])

#PCA

from sklearn.preprocessing import StandardScaler
X_std = StandardScaler().fit_transform(X)
import numpy as np
mean_vec = np.mean(X_std, axis=0)
cov_mat = (X_std - mean_vec).T.dot((X_std - mean_vec)) / (X_std.shape[0]-1)
print('Covariance matrix \n%s' %cov_mat)
eig_vals, eig_vecs = np.linalg.eig(cov_mat)
print('\nEigenvalues \n%s' %eig_vals)
eig_tups = [(eig_vals[i],i) for i in range(len(eig_vals))]

eig_tups.sort(reverse=True)
print eig_tups

import plotly.plotly as py
from plotly.graph_objs import *
import plotly.tools as tls

tot = sum(eig_vals)
var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
cum_var_exp = np.cumsum(var_exp)

trace1 = Bar(
        x=['PC %s' %i for i in range(1,len(eig_vals))],
        y=var_exp,
        showlegend=False)

trace2 = Scatter(
        x=['PC %s' %i for i in range(1,len(eig_vals))],
        y=cum_var_exp,
        name='cumulative explained variance')

data = Data([trace1, trace2])

layout=Layout(
        yaxis=YAxis(title='Explained variance in percent'),
        title='Explained variance by different principal components')

py.image.save_as({'data':data}, 'dental_explained_variance.png')
fig = Figure(data=data, layout=layout)
py.iplot(fig)

# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs.sort()
eig_pairs.reverse()

matrix_w = np.hstack((eig_pairs[0][1].reshape(len(eig_vals),1), 
                      eig_pairs[1][1].reshape(len(eig_vals),1)))

print('Matrix W:\n', matrix_w)

#Y = X_std.dot(matrix_w)
Y = X_std.dot(matrix_w)

#project in 2 dimensions
traces = []

names = ('Inactive', 'Active')
for i in range(0,2):

    trace = Scatter(
        x=Y[y==i,0],
        y=Y[y==i,1],
        mode='markers',
        name=names[i],
        marker=Marker(
            size=12,
            line=Line(
                color='rgba(217, 217, 217, 0.14)',
                width=0.5),
            opacity=0.8))
    traces.append(trace)


data = Data(traces)
layout = Layout(showlegend=True,
                scene=Scene(xaxis=XAxis(title='PC1'),
                yaxis=YAxis(title='PC2'),))
py.image.save_as({'data':data}, 'dental_projected_2d.png')
fig = Figure(data=data, layout=layout)
py.iplot(fig)


