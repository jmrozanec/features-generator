import abc
import os

# https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python

# represents the product created by the builder.
class Car:
    def __init__(self):
        self.color = None

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def __str__(self):
        return "Car [color={0}]".format(self.color)


# the builder abstraction
class CarBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_color(self, color):
        pass

    @abc.abstractmethod
    def get_result(self):
        pass


class CarBuilderImpl(CarBuilder):
    def __init__(self):
        self.car = Car()

    def set_color(self, color):
        self.car.set_color(color)

    def get_result(self):
        return self.car


class CarBuildDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct(self):
        self.builder.set_color("Red");
        return self.builder.get_result()

if __name__ == '__main__':
    builder = CarBuilderImpl()
    carBuildDirector = CarBuildDirector(builder)
    print(carBuildDirector.construct())


class CreateKeyDataframeAction():
    def __init__(self, key_name=None, columns=None):
        self.key_name = None
        self.columns = None

class SquashNumericDataframeAction():
    def __init__(self, key_name=None, squash_strategy=None):
        self.key_name = key_name
        self.squash_strategy = squash_strategy

class JoinDataframeAction():
    def __init__(self, key_name=None, squash_strategy=None):
        self.key_name = key_name
        self.squash_strategy = squash_strategy



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

# the builder abstraction
class ExperimentBuilder(metaclass=abc.ABCMeta):
    def __init__(self):
        self.steps = []

    @abc.abstractmethod
    def load_dataframe(self, dataset_path):
        step = DataframeBuilder(self, dataset_path)
        self.steps.append(step)
        return step

    @abc.abstractmethod
    def inner_join(self, left_df_name, right_df_name, columns_left, columns_right):
        step = JoinBuilder(self, "inner", left_df_name, right_df_name, columns_left, columns_right)
        self.steps.append(step)
        return step

    @abc.abstractmethod
    def for_dataframe(self, dataframe):
        pass





    @abc.abstractmethod
    def get_result(self):
        pass


 class ExperimentBuilderImpl(ExperimentBuilder):
    def __init__(self):
        self.car = Car()

    def set_color(self, color):
        self.car.set_color(color)

    def get_result(self):
        return self.car


squash_strategy=mean, sum


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


