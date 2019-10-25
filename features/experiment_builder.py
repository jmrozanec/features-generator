import abc
import os

# https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python

class CreateKeyDataframeAction():
    def __init__(self, key_name=None, columns=None):
        self.key_name = None
        self.columns = None

class SquashNumericDataframeAction():
    def __init__(self, key_name=None, squash_strategy=None):
        self.key_name = key_name
        self.squash_strategy = squash_strategy

# TODO!
class JoinDataframeAction():
    def __init__(self, key_name=None, squash_strategy=None):
        self.key_name = key_name
        self.squash_strategy = squash_strategy

class RemoveDummyColsDataframeAction():
    def __init__(self, df_name):
        self.df_name = df_name

class DataframeBuilder():
    def __init__(self, experiment_builder, dataset_path):
        self.experiment_builder = experiment_builder
        self.dataset_path = dataset_path
        base=os.path.basename(dataset_path)
        self.df_name = os.path.splitext(base)[0]
        self.actions = []

    def as(self, df_name):
        self.df_name = df_name
        return self

    def with_key(self, columns):
        self.actions.append(CreateKeyDataframeAction(key_name=key_name, columns=columns))
        return self

    def squash_numeric(self, key_name, squash_strategy):
        self.actions.append(SquashNumericDataframeAction(key_name=key_name, squash_strategy=squash_strategy))
        return self

    def remove_dummy_cols():
        pass

    def remove_dummy_rows():
        pass

    def create_lag_features():
        pass

    def ratio_for_lagged():
        pass

    def and():
        return self.experiment_builder

class JoinBuilder():
    def __init__(self, experiment_builder, join_type, left_df_name, right_df_name, columns_left, columns_right):
        self.experiment_builder = experiment_builder
        self.action = JoinDataframeAction(join_type, left_df_name, right_df_name, columns_left, columns_right)
        self.df_name = "{}-{}-{}".format(left_df_name, join_type, right_df_name)

    def as(self, df_name):
        self.df_name = df_name
        return self

    def and():
        return self.experiment_builder

class DatasetSplitBuilder():
    def __init__(self, experiment_builder, split_type, val, test):
        self.experiment_builder = experiment_builder
        self.split_type = split_type
        self.val = val
        self.test = test

    def build(): #TODO rename to method when applied cross actions
        if (type(val) != type(test)):
            print("Types for val and test should be the same") # TODO throw an error
        else:
            if (type(val) == "int" || type(val) == "float"):
                return None # return corresponding action
            if (type(val) == "datetime.timedelta"):
                return None # return corresponding action

# TODO put into another package
class ModelTrainBuilder():
    def __init__(self, builder, ):

    def with_validation_metrics():
        print("ModelTrainBuilder::with_validation_metrics()")

    def saving_best():
        print("ModelTrainBuilder::saving_best()")

class ModelTestBuilder():
    def __init__(self, builder, ):

    def with_test_metrics():
        print("ModelTrainBuilder::with_test_metrics()")

class GBRegressorBuilder():
    def __init__(self):
        self.params = {}

    def with_colsample_bytree(colsample_bytree):
        self.params['colsample_bytree']=colsample_bytree
        return self

    def with_gamma(gamma):
        self.params['gamma']=gamma
        return self

    def with_learning_rate(learning_rate):
        self.params['learning_rate']=learning_rate
        return self

    def with_max_depth(max_depth):
        self.params['max_depth']=max_depth
        return self

    def with_min_child_weight(min_child_weight):
        self.params['min_child_weight']=min_child_weight
        return self

    def with_estimators(estimators):
        self.params['estimators']=estimators
        return self

    def with_reg_alpha(reg_alpha):
        self.params['reg_alpha']=reg_alpha
        return self

    def with_reg_lambda(reg_lambda):
        self.params['reg_lambda']=reg_lambda
        return self

    def with_subsample(subsample):
        self.params['subsample']=subsample
        return self

    def and():



# the builder abstraction
class ExperimentBuilder():
    def __init__(self):
        self.steps = []
        self.steps.append() # TODO: set seed

    def set_seed(self, seed: 1234):


    def load_dataframe(self, dataset_path):
        step = DataframeBuilder(self, dataset_path)
        self.steps.append(step)
        return step

    def join(self, join_type, left_df_name, right_df_name, columns_left, columns_right):
        step = JoinBuilder(self, join_type, left_df_name, right_df_name, columns_left, columns_right)
        self.steps.append(step)
        return step

    # We shall accept val/test: https://docs.python.org/3/library/datetime.html#datetime.timedelta
    # 
    def split_trainvaltest(val=0.1, test=0.2):
        step = DatasetSplitBuilder(self, val, test)
        self.steps.append(step)
        return step

    def create_model(model_type):
        if(model_type == 'gbr'):
            return GBRegressorBuilder()

    def train():
        step = TrainAbstractionBuilder()
        self.steps.append(step)
        return step

    def execute():

    def report():

    def summary():
        # TODO create a summary report considering ex.: involved datasets and configurations.






# squash_strategy=mean, sum


ExperimentBuilder()
   .load_dataframe('cars', '/home/datasets/cars.csv').with_key(key_name, [columns]).squash_numeric('dm-key', squash_strategy)
   .load_dataframe('trains', '/home/datasets/cars.csv').with_key(key_name)
   .inner_join(left, right, columns_left, columns_right)
   .create_lag_features(column, prefix, lag_range)
   .ratio_for_lagged([columns], lagged_column_prefix, source_lag_range, target_offset, target_lag_range_end)



ExperimentBuilder()
   .load_dataframe('/home/datasets/cars.csv').with_key(key_name, [columns]).squash_numeric('dm-key', squash_strategy).as('cars') -> dataframe builder
   .and() -> experiment builder
   .load_dataframe('trains', '/home/datasets/cars.csv').with_key(key_name).and()
   .create_dataframe_as_join('df1', [left], [right], columns_left, columns_right) -> experiment builder
   .for('df1') -> dataframe builder
   .create_lag_features(column, prefix, lag_range) -> dataframe builder
   .ratio_for_lagged([columns], lagged_column_prefix, source_lag_range, target_offset, target_lag_range_end) -> dataframe builder
   .split_trainvaltest(val=0.1, test=0.2, policy='last')            # TODO: we should randomize the dataset and get the required splits
   .split_trainvaltest(val=1.month, test=2.months, policy='any')    # TODO: we should take required amount of months (months selected randomly) and then randomize each part
   .split_trainvaltest(val=1.month, test=2.months, policy='last')   # TODO: we should sort by date if policy is 'last' and after division randomize each part
   .normalize().and() # TODO: auto-normalize or set manually?
   .feature_selection().and()
   .create_model('gbt').and()
   .train().with_validation_metrics().saving_best().and()
   .test().with_test_metrics().and()
   .report()
   .execute()

