import numpy as np
import pandas as pd
import os
from factorbase import FactorBase
from operation import Operation
import basicfunc

class FactorPool(FactorBase):
    """Class ``FactorPool`` inherites from ``FactorBase`` and represents a pool
    of factors used for alpha generation.
    
    .. note:: 

        If you want to use base feature that is not in the ``BASEDATA`` folder(higher dimensional features),
        please specify the folder name to which the feature belongs in dict ``self.need_hdim_fields``.

            | Example: ``"ASHAREBALANCESHEET": ["ACC_EXP", "ACC_PAYABLE"]``,
            | key-value pair structure as follows:
            | ``key``: ``sheet_name``,
            | ``value``: ``list of feature fields``.

    .. warning::
        Caution: Please ``ONLY`` load the feature that you need to avoid potential problem.
    
    Parameters
    ----------
    start_date : str
        Start date for backtesting.
    end_date: str
        End date for backtesting.
    winsorize : bool
        Flag indcating wether to `winsorize` data.
    zscore : bool
        Flag indicating whether to `z-score` normalize data.
    ind_neu : bool
        Flag indicating whether to perform `industry neutralization`.
    fillna : bool
        Flag indicating whether to fill ``NaN`` and ``Inf`` values in data.
    
    need_fields : list
        List of base features needed for alpha generation.

        e.g ``PV features: ["OPEN", "CLOSE", "TOP300"]``, return shape: ``[days, tickers]``
    need_hdim_fields: dict
        Dictionary containing high dimensional features needed for alpha generation.

        e.g. ``High dimensional features: AShareIncome/AShareBalanceSheet/..``,

    Examples
    ----------
    Alpha definition

    1. base feature gneration:
        
        index with no shit: ``startdi - delay`` ~ ``enddi - startdi + 1``
    
    2. alpha logic calculation:
        | Mapping:
        | ``func name`` -> ``alpha name``
        | ``return value`` -> ``alpha value(ndarray)``

    Gnerate with this rule automatically

    >>> def factor_name(self):
    ...   # factor description and specific expression etc.
    ...   feat1 = self.need_data['FEAT1']
    ...   feat2 = self.need_data['FEAT2']
    ...   alpha = feat1 + feat2
    ...   return alpha
    """

    def __init__(self):
        super(FactorPool, self).__init__()
        # Set Backtesting Date
        self.start_date = "20190303"
        self.end_date = "20231231"

        # preprocessing
        self.winsorize = False
        self.zscore = False
        self.ind_neu = True
        self.fillna = False

        self.need_fields = [
            "OPEN",
            "CLOSE",
            "VOL",
            "HIGH",
            "LOW",
            "VWAP"
        ]

    def alpha_1(self):
        high = self.need_data["HIGH"]
        low = self.need_data["LOW"]
        alpha = Operation.rolling_std((high - low), 5)
        return alpha

    def alpha_2(self):
        high = self.need_data["HIGH"]
        low = self.need_data["LOW"]
        alpha = Operation.rolling_std((high - low), 10)
        return alpha

    def alpha_3(self):
        close = self.need_data["CLOSE"]
        alpha = Operation.rolling_std(close, 5)
        return alpha
        

if __name__ == "__main__":
    fpool = FactorPool()
    fpool.execute_alphaflow(group_detail="on", prefix="votality", stockwise_export="off", invert=True)
    print(f"Test range: {fpool.start_date} ~ {fpool.end_date}")
    print(f"Test range: {fpool.actdays[0]} ~ {fpool.actdays[-1]}")
    



