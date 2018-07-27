from sklearn.base import BaseEstimator, TransformerMixin
from feature_generation_strategy import MinFeatureGenerationStrategy, MaxFeatureGenerationStrategy, SumFeatureGenerationStrategy, DiffFeatureGenerationStrategy, ProdFeatureGenerationStrategy, DivFeatureGenerationStrategy, AvgFeatureGenerationStrategy, PCAFeatureGenerationStrategy, TSVDFeatureGenerationStrategy, ICAFeatureGenerationStrategy, GRPFeatureGenerationStrategy, SRPFeatureGenerationStrategy

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


class FeatureGenerator(BaseEstimator, TransformerMixin):
    """
    Feature generator: enables to create features using provided strategies.
    """
    def __init__(self, key, strategies):
        self.key = key
        self.strategies = strategies

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]







iris = load_iris()
df = pd.DataFrame(data= np.c_[iris['data'], iris['target']], columns= iris['feature_names'] + ['target'])
train, X_valtest, y_train, y_valtest = train_test_split(df[df.columns.difference(['target'])], df['target'], test_size=0.3)
val, test, y_val, y_test = train_test_split(X_valtest, y_valtest, test_size=0.5)

column_names = train.columns.values
minstrat = MinFeatureGenerationStrategy()
maxstrat = MaxFeatureGenerationStrategy()
sumstrat = SumFeatureGenerationStrategy()
diffstrat = DiffFeatureGenerationStrategy()
prodstrat = ProdFeatureGenerationStrategy()
divstrat = DivFeatureGenerationStrategy()
avgstrat = AvgFeatureGenerationStrategy()
pcastrat = PCAFeatureGenerationStrategy()
tsvdstrat = TSVDFeatureGenerationStrategy()
icastrat = ICAFeatureGenerationStrategy()
grpstrat = GRPFeatureGenerationStrategy()
srpstrat = SRPFeatureGenerationStrategy()

strategies1 = [minstrat, maxstrat, sumstrat, diffstrat, prodstrat, divstrat, avgstrat]
strategies2 = [pcastrat, tsvdstrat, icastrat, grpstrat, srpstrat]

def generate_features(train, val, test, colname1, colname2, strategies):
	for strategy in strategies:
		train, val, test = strategy.generate(train, val, test, colname1, colname2)
	return (train, val, test)

for colname1 in column_names:
	for colname2 in column_names:
		train, val, test = generate_features(train, val, test, colname1, colname2, strategies1)

train.fillna(0, inplace=True)
val.fillna(0, inplace=True)
test.fillna(0, inplace=True)

for strategy in strategies2:
	train, val, test = strategy.generate(train, val, test, 10)

new_column_names = train.columns.values
print("original columns: {}".format(",".join(column_names)))
print("new columns: {}".format(",".join(new_column_names)))
