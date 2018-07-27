# Adversarial validation
# Taken from: https://www.kaggle.com/kevinbonnes/adversarial-validation
import numpy as np
import pandas as pd
import gc
import datetime

from sklearn.model_selection import KFold
import lightgbm as lgb

# Params
NFOLD = 5
DATA_PATH = '.'
# Load data
train = pd.read_csv(DATA_PATH + "train.csv")
test = pd.read_csv(DATA_PATH + "test.csv")

# Mark train as 1, test as 0
train['target'] = 1
test['target'] = 0

# Concat dataframes
n_train = train.shape[0]
df = pd.concat([train, test], axis = 0)
del train, test
gc.collect()

# Remove columns with only one value in our training set
predictors = list(df.columns.difference(['ID', 'target']))
df_train = df.iloc[:n_train].copy()
cols_to_remove = [c for c in predictors if df_train[c].nunique() == 1]
df.drop(cols_to_remove, axis=1, inplace=True)

# Update column names
predictors = list(df.columns.difference(['ID', 'target']))

# Get some basic meta features
df['cols_mean'] = df[predictors].replace(0, np.NaN).mean(axis=1)
df['cols_count'] = df[predictors].replace(0, np.NaN).count(axis=1)
df['cols_sum'] = df[predictors].replace(0, np.NaN).sum(axis=1)
df['cols_std'] = df[predictors].replace(0, np.NaN).std(axis=1)

# Prepare for training

# Shuffle dataset
df = df.iloc[np.random.permutation(len(df))]
df.reset_index(drop = True, inplace = True)

# Get target column name
target = 'target'

# lgb params
lgb_params = {
        'boosting': 'gbdt',
        'application': 'binary',
        'metric': 'auc', 
        'learning_rate': 0.1,
        'num_leaves': 32,
        'max_depth': 8,
        'bagging_fraction': 0.7,
        'bagging_freq': 5,
        'feature_fraction': 0.7,
}

# Get folds for k-fold CV
folds = KFold(n_splits = NFOLD, shuffle = True, random_state = 0)
fold = folds.split(df)
    
eval_score = 0
n_estimators = 0
eval_preds = np.zeros(df.shape[0])

# Run LightGBM for each fold
for i, (train_index, test_index) in enumerate(fold):
    print( "\n[{}] Fold {} of {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), i+1, NFOLD))
    train_X, valid_X = df[predictors].values[train_index], df[predictors].values[test_index]
    train_y, valid_y = df[target].values[train_index], df[target].values[test_index]

    dtrain = lgb.Dataset(train_X, label = train_y,
                          feature_name = list(predictors)
                          )
    dvalid = lgb.Dataset(valid_X, label = valid_y,
                          feature_name = list(predictors)
                          )
        
    eval_results = {}
    
    bst = lgb.train(lgb_params, 
                         dtrain, 
                         valid_sets = [dtrain, dvalid], 
                         valid_names = ['train', 'valid'], 
                         evals_result = eval_results, 
                         num_boost_round = 5000,
                         early_stopping_rounds = 100,
                         verbose_eval = 100)
    
    print("\nRounds:", bst.best_iteration)
    print("AUC: ", eval_results['valid']['auc'][bst.best_iteration-1])

    n_estimators += bst.best_iteration
    eval_score += eval_results['valid']['auc'][bst.best_iteration-1]
   
    eval_preds[test_index] += bst.predict(valid_X, num_iteration = bst.best_iteration)
    
n_estimators = int(round(n_estimators/NFOLD,0))
eval_score = round(eval_score/NFOLD,6)

print("\nModel Report")
print("Rounds: ", n_estimators)
print("AUC: ", eval_score)

df_av = df[['ID', 'target']].copy()
df_av['preds'] = eval_preds
df_av_train = df_av[df_av.target == 1]
df_av_train = df_av_train.sort_values(by=['preds']).reset_index(drop=True)

topN=1000
df.head(topN).to_csv('validation.csv')
