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
