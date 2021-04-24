from data_acquisition import read_input_data
from strategy import simulate_strategy, store_sim_data

# ----------------
# -- Parameters --
# ----------------
STOCK_INDEX     = 'FSX'
EXPIRATION_TIME = "12:30:00"
WINDOW_STEP     =   2
MIN_IN_WINDOW   =   0
MAX_IN_WINDOW   = 200 + WINDOW_STEP
MIN_OUT_WINDOW  = -40
MAX_OUT_WINDOW  = 200 + WINDOW_STEP

# ----------------------------------------
# -- Data acquisition and preprocessing --
# ----------------------------------------
raw_data = read_input_data(STOCK_INDEX, remove_NaNs = False)

# [2010 - 2021]
df = raw_data[raw_data.index >= '2010-01-01']

# ---------------------
# -- Data generation --
# ---------------------
for in_window in range(MIN_IN_WINDOW, MAX_IN_WINDOW, WINDOW_STEP):
    for out_window in range(MIN_OUT_WINDOW, MAX_OUT_WINDOW, WINDOW_STEP):
        # Skip meaningless setups
        if (out_window >= 0) or (in_window >= abs(out_window)):
            print('Simulating [{}, {}]'.format(in_window, out_window))
            dates, returns = simulate_strategy(df, EXPIRATION_TIME, in_window, out_window)
            store_sim_data(in_window, out_window, dates, returns)