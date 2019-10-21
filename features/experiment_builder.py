import abc

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


class DataframeKeyAction():
    def __init__(self):
        self.name = None
        self.data_path = None
        self.actions = []

class DataframeSquashNumericAction():




class DataframeBuilder(metaclass=abc.ABCMeta):
    def __init__(self):
        self.name = None
        self.data_path = None
        self.actions = []


    @abc.abstractmethod
    def with_key(self, dataframe, name):
        return self    


# the builder abstraction
class ExperimentBuilder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def load_dataframe_as(self, name, data_path):
        self.name = name
        self.data_path = data_path
        return self

    @abc.abstractmethod
    def load_dataframe_as(self, dataframe, name):

        pass  

    @abc.abstractmethod
    def for_dataframe(self, dataframe):
        pass

    @abc.abstractmethod
    def remove_dummy_cols():
        pass

    @abc.abstractmethod
    def remove_dummy_rows():
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




