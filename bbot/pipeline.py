"""

Concept API

Pipeline requires functions that calculate features
A feature function must return one of the following datatypes:
-list  -> gets merged as a key in every candle in candlelist
-nparr -> idem, must be 1-dimensional or 2dimensional with one column
-df    -> idem

or

-dict  -> a single candle, that replaces last candle in list of candles OR a single value featurename:value that gets inserted in last candle
-tuple -> in the form (featurename, value) that gets inserted in last candle

TODO: feature calculation functions need access to realtime data. This data is provided by bbot class.
Thats why pipeline cannot be argument in Options class, which is used in init function of bbot class...
Instead something like bot.add_pipeline(p)

"""
import numpy as np
import pandas as pd
import itertools

# feature1(bot)
def feature1():
    print('First feature')


def feature2():
    print('Second feature')


def feature3():
    print('Third feature')


class Pipeline():

    def _insert_db_ref(self, db):
        self.db = db
        self.features = []

    def __or__(self, feature):
        self._calc_feature(feature)
        self.features.append(feature)
        return self

    def _calc_feature(self, feature):
        '''Calculate feature for the first time on all historical candles'''
        try:
            r = feature()
            if type(r) is list:
                self._verify_list(r)
                self._merge_list(r)
            elif type(r) is np.array:
                self._verify_np_arr(r)
                self._merge_np_arr(r)
            elif type(r) is pd.DataFrame:
                self._verify_df(r)
                self._merge_df(r)
            elif type(r) is dict:
                self._verify_dict(r)
                self._merge_dict(r)
            elif type(r) is tuple:
                self._verify_tuple(r)
                self._merge_tuple(r)
            else:
                e = f'''The return value of feature {feature} has the wrong type.
                     It should be a list, numpy array, pandas dataframe, dict or tuple.'''
                raise Exception(e)
        except:
            raise Exception(
                f'Feature {feature} throws an exception during initialization.')



    def _verify_list(self, f):
        counter = itertools.count(0)
        [(next(counter), i) for i in f if type(i) is not float]
        if counter > 0:
            w = f'''Warning: Not every item in the return value of {f} is a float.
                 You might want to convert it for use in a machine learning model.'''
            print(w)


    def _verify_np_arr(self, f):
        pass

    def _verify_df(self, f):
        pass

    def _verify_dict(self, f):
        pass

    def _verify_tuple(self, f):
        pass

    def _merge_list(self, f):
        pass

    def _merge_np_arr(self, f):
        pass

    def _merge_df(self, f):
        pass

    def _merge_dict(self, f):
        pass

    def _merge_tuple(self, f):
        pass


# ------------------------------------------------------------------
# Usage:

p = Pipeline() | feature1 \
               | feature2 \
               | feature3
