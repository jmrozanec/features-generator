from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA, TruncatedSVD, FastICA
from sklearn.random_projection import GaussianRandomProjection, SparseRandomProjection
import abc

class ColumnBasedFeatureGenerationStrategyAbstract(BaseEstimator, TransformerMixin):
    """Provides abstraction for features generation"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def fit(self, train):
        """Required Method"""

    @abc.abstractmethod
    def transform(self, train):
        """Required Method"""

    @abc.abstractmethod
    def featurename(self, colname1, colname2):
        """Required Method"""

    @abc.abstractmethod
    def equivalent_featurenames(self, colname1, colname2):
        """Required Method. Used to reflect commutativity."""

class SumFeatureGenerationStrategy(ColumnBasedFeatureGenerationStrategyAbstract):
    def fit(self, train, val, test, colname1, colname2):
        train[self.featurename(colname1, colname2)] = train[[colname1, colname2]].sum(axis=1)
        val[self.featurename(colname1, colname2)] = val[[colname1, colname2]].sum(axis=1)
        test[self.featurename(colname1, colname2)] = test[[colname1, colname2]].sum(axis=1)
        return (train, val, test)

    def featurename(self, colname1, colname2):
        return "{}_sum_{}".format(colname1, colname2)

    def equivalent_featurenames(self, colname1, colname2):
        return [self.featurename(colname1, colname2), self.featurename(colname2, colname1)]


class DiffFeatureGenerationStrategy(ColumnBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, colname1, colname2):
        train[self.featurename(colname1, colname2)]=train[colname1]-train[colname2]
        val[self.featurename(colname1, colname2)]=train[colname1]-val[colname2]
        test[self.featurename(colname1, colname2)]=test[colname1]-test[colname2]
        return (train, val, test)

    def featurename(self, colname1, colname2):
        return "{}_diff_{}".format(colname1, colname2)

    def equivalent_featurenames(self, colname1, colname2):
        return [self.featurename(colname1, colname2)]

class ProdFeatureGenerationStrategy(ColumnBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, colname1, colname2):
        train[self.featurename(colname1, colname2)]=train[colname1]*train[colname2]
        val[self.featurename(colname1, colname2)]=val[colname1]*val[colname2]
        test[self.featurename(colname1, colname2)]=test[colname1]*test[colname2]
        return (train, val, test)

    def featurename(self, colname1, colname2):
        return "{}_prod_{}".format(colname1, colname2)

    def equivalent_featurenames(self, colname1, colname2):
        return [self.featurename(colname1, colname2), self.featurename(colname2, colname1)]

class DivFeatureGenerationStrategy(ColumnBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, colname1, colname2):
        train[self.featurename(colname1, colname2)]=train[colname1]/train[colname2]
        val[self.featurename(colname1, colname2)]=val[colname1]/val[colname2]
        test[self.featurename(colname1, colname2)]=test[colname1]/test[colname2]
        return (train, val, test)

    def featurename(self, colname1, colname2):
        return "{}_div_{}".format(colname1, colname2)

    def equivalent_featurenames(self, colname1, colname2):
        return [self.featurename(colname1, colname2)]

class AvgFeatureGenerationStrategy(ColumnBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, colname1, colname2):
        train[self.featurename(colname1, colname2)]=train[[colname1, colname2]].mean(axis=1)
        val[self.featurename(colname1, colname2)]=val[[colname1, colname2]].mean(axis=1)
        test[self.featurename(colname1, colname2)]=test[[colname1, colname2]].mean(axis=1)
        return (train, val, test)

    def featurename(self, colname1, colname2):
        return "{}_avg_{}".format(colname1, colname2)

    def equivalent_featurenames(self, colname1, colname2):
        return [self.featurename(colname1, colname2), self.featurename(colname2, colname1)]

class MaxFeatureGenerationStrategy(ColumnBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, colname1, colname2):
        train[self.featurename(colname1, colname2)]=train[[colname1, colname2]].max(axis=1)
        val[self.featurename(colname1, colname2)]=val[[colname1, colname2]].max(axis=1)
        test[self.featurename(colname1, colname2)]=test[[colname1, colname2]].max(axis=1)
        return (train, val, test)

    def featurename(self, colname1, colname2):
        return "{}_max_{}".format(colname1, colname2)

    def equivalent_featurenames(self, colname1, colname2):
        return [self.featurename(colname1, colname2), self.featurename(colname2, colname1)]

class MinFeatureGenerationStrategy(ColumnBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, colname1, colname2):
        train[self.featurename(colname1, colname2)]=train[[colname1, colname2]].min(axis=1)
        val[self.featurename(colname1, colname2)]=val[[colname1, colname2]].min(axis=1)
        test[self.featurename(colname1, colname2)]=test[[colname1, colname2]].min(axis=1)
        return (train, val, test)

    def featurename(self, colname1, colname2):
        return "{}_min_{}".format(colname1, colname2)

    def equivalent_featurenames(self, colname1, colname2):
        return [self.featurename(colname1, colname2), self.featurename(colname2, colname1)]

# Features based on decomposition methods
class DecompositionBasedFeatureGenerationStrategyAbstract(object):
    """Provides abstraction for features generation"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate(self, train, val, test):
        """Required Method"""

    @abc.abstractmethod
    def featurename(self, idx):
        """Required Method"""

    @abc.abstractmethod
    def equivalent_featurenames(self, idx):
        """Required Method. Used to reflect commutativity."""


class PCAFeatureGenerationStrategy(DecompositionBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, n_comps):
        decomposer = PCA(n_components=n_comps, random_state=1234)
        results_train = decomposer.fit_transform(train)
        results_val = decomposer.fit_transform(val)
        results_test = decomposer.transform(test)
        for i in range(1, n_comps + 1):
            train[self.featurename(i)] = results_train[:, i - 1]
            val[self.featurename(i)] = results_val[:, i - 1]
            test[self.featurename(i)] = results_test[:, i - 1]
        return (train, val, test)

    def featurename(self, idx):
        return "pca_{}".format(str(idx))

    def equivalent_featurenames(self, idx):
        return [self.featurename(idx)]

class TSVDFeatureGenerationStrategy(DecompositionBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, n_comps):
        decomposer = TruncatedSVD(n_components=n_comps, random_state=1234)
        results_train = decomposer.fit_transform(train)
        results_val = decomposer.fit_transform(val)
        results_test = decomposer.transform(test)
        for i in range(1, n_comps + 1):
            train[self.featurename(i)] = results_train[:, i - 1]
            val[self.featurename(i)] = results_val[:, i - 1]
            test[self.featurename(i)] = results_test[:, i - 1]
        return (train, val, test)

    def featurename(self, idx):
        return "tsvd_{}".format(str(idx))

    def equivalent_featurenames(self, idx):
        return [self.featurename(idx)]

class ICAFeatureGenerationStrategy(DecompositionBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, n_comps):
        decomposer = FastICA(n_components=n_comps, random_state=1234)
        results_train = decomposer.fit_transform(train)
        results_val = decomposer.fit_transform(val)
        results_test = decomposer.transform(test)
        for i in range(1, n_comps + 1):
            train[self.featurename(i)] = results_train[:, i - 1]
            val[self.featurename(i)] = results_val[:, i - 1]
            test[self.featurename(i)] = results_test[:, i - 1]
        return (train, val, test)

    def featurename(self, idx):
        return "ica_{}".format(str(idx))

    def equivalent_featurenames(self, idx):
        return [self.featurename(idx)]

class GRPFeatureGenerationStrategy(DecompositionBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, n_comps):
        decomposer = GaussianRandomProjection(n_components=n_comps, random_state=1234)
        results_train = decomposer.fit_transform(train)
        results_val = decomposer.fit_transform(val)
        results_test = decomposer.transform(test)
        for i in range(1, n_comps + 1):
            train[self.featurename(i)] = results_train[:, i - 1]
            val[self.featurename(i)] = results_val[:, i - 1]
            test[self.featurename(i)] = results_test[:, i - 1]
        return (train, val, test)

    def featurename(self, idx):
        return "grp_{}".format(str(idx))

    def equivalent_featurenames(self, idx):
        return [self.featurename(idx)]

class SRPFeatureGenerationStrategy(DecompositionBasedFeatureGenerationStrategyAbstract):
    def generate(self, train, val, test, n_comps):
        decomposer = SparseRandomProjection(n_components=n_comps, random_state=1234)
        results_train = decomposer.fit_transform(train)
        results_val = decomposer.fit_transform(val)
        results_test = decomposer.transform(test)
        for i in range(1, n_comps + 1):
            train[self.featurename(i)] = results_train[:, i - 1]
            val[self.featurename(i)] = results_val[:, i - 1]
            test[self.featurename(i)] = results_test[:, i - 1]
        return (train, val, test)

    def featurename(self, idx):
        return "grp_{}".format(str(idx))

    def equivalent_featurenames(self, idx):
        return [self.featurename(idx)]
