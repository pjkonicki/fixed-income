import datetime
import unittest

import numpy as np
import pandas as pd
import vcr

from fixed_income import data


class TestTreasuryDirect(unittest.TestCase):
    date = datetime.date(year=2017, month=11, day=17)
    test_data = {'BUY': {0: '97.500000', 1: '99.156250'},
                 'CALL DATE': {0: np.nan, 1: np.nan},
                 'CUSIP': {0: '912828K74', 1: '912828M56'},
                 'END OF DAY': {0: '97.562500', 1: '99.218750'},
                 'MATURITY': {0: 7.6743533405887865, 1: 7.9262407852317294},
                 'MATURITY DATE': {0: pd.Timestamp('2025-08-15 00:00:00'),
                                   1: pd.Timestamp('2025-11-15 00:00:00')},
                 'RATE': {0: '2.000%', 1: '2.250%'},
                 'SECURITY TYPE': {0: 'MARKET BASED NOTE', 1: 'MARKET BASED NOTE'},
                 'SELL': {0: '97.500000', 1: '99.156250'}}

    @vcr.use_cassette('resources/test_load_data_from_date.yml')
    def test_load_data_from_date(self):
        df = data.treasury_direct(self.date)
        self.assertTrue(~df.empty)

    def test_get_cashflows(self):
        quote_date = datetime.date(year=2017, month=12, day=12)
        df = pd.DataFrame(self.test_data)
        expected_cashflows = np.array([[1.125, 1.125, 1.125, 1.125, 1.125, 1.125,
                                        1.125, 1.125, 1.125, 1.125, 1.125, 1.125,
                                        1.125, 1.125, 1.125, 101.125],
                                       [1., 1., 1., 1., 1., 1.,
                                        1., 1., 1., 1., 1., 1.,
                                        1., 1., 1., 101.]])
        expected_maturities = np.array([[0.42624079, 0.92624079, 1.42624079, 1.92624079, 2.42624079,
                                         2.92624079, 3.42624079, 3.92624079, 4.42624079, 4.92624079,
                                         5.42624079, 5.92624079, 6.42624079, 6.92624079, 7.42624079,
                                         7.92624079],
                                        [0.17435334, 0.67435334, 1.17435334, 1.67435334, 2.17435334,
                                         2.67435334, 3.17435334, 3.67435334, 4.17435334, 4.67435334,
                                         5.17435334, 5.67435334, 6.17435334, 6.67435334, 7.17435334,
                                         7.67435334]])

        actual_cashflows, actual_maturities = data.cashflows_matrix(df, quote_date)
        self.assertTrue(np.array_equal(expected_cashflows, actual_cashflows))
        self.assertTrue(np.allclose(expected_maturities, actual_maturities, rtol=1e-7))
