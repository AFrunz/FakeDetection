from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle
#
#
# def get_pred(a):
#     dataset = pd.read_csv('data_base_new.csv', delimiter=',', index_col=0)
#     train_x = dataset[
#         ['friends', 'followers', 'wall', 'groups', 'subscriptions', 'nick', 'photo', 'audio', 'presents', 'video',
#          'face', 'school_count', 'link in 1th post', 'city',
#          'learn_place']]
#     train_y = dataset['fake']
#     Tree = RandomForestClassifier(n_estimators=1000)
#     Tree.fit(train_x, train_y)
#     a = a.reshape(1, -1)
#     pred = Tree.predict(a)
#     return pred


def get_pred1(a):
    file = open('Tree.h5', 'rb')
    Tree = pickle.load(file)
    a = a.reshape(1, -1)
    pred = Tree.predict(a)
    return pred
