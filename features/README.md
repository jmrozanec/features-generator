Pipeline interface, compatible with scikit
- we can drop all columns that provide no information
- we can analyze most important features for given columns
- we create new features from given columns (strategies)

def drop_sparse(train, test):
    flist = [x for x in train.columns if not x in ['ID','target']]
    for f in flist:
        if len(np.unique(train[f]))<2:
            train.drop(f, axis=1, inplace=True)
            test.drop(f, axis=1, inplace=True)
    return train, test


set the seed, export results uniformly, persist joined datasets so we can make better use in a future, provide hashed tmp files over original paths and definitions, so we always get the same working again :)
this should work as a wrp

ExperimentBuilder()
   .load_dataframe('cars', '/home/datasets/cars.csv').with_key(key_name, [columns]).squash_numeric('dm-key', squash_strategy)
   .load_dataframe('trains', '/home/datasets/cars.csv').with_key(key_name)
   .inner_join(left, right, columns_left, columns_right)
   .create_lag_features(column, prefix, lag_range)
   .ratio_for_lagged([columns], lagged_column_prefix, source_lag_range, target_offset, target_lag_range_end)
