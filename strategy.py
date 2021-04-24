import numpy as np
import datetime
import pandas as pd

def get_next_expiration(df, date):
    quarterly_months = [3, 6, 9, 12]
    
    # 3rd friday is known to be between 15th and 21st
    return df[(df.index.date  >  date)               &
              (df.index.day   >= 15)                 &
              (df.index.day   <= 21)                 &
              (df.day_of_week == 'Friday')           &
              (df.index.month.isin(quarterly_months))]

def simulate_strategy(df, expiration_time, in_window, out_window):
    trades_return   = []
    trades_dates    = []
    expiration_rows = df.copy()
    
    # Trading log
    f_log = open('./log/trades' + '_' + str(in_window) + '_' + str(out_window) + '.log', 'w')

    # Get all rows corresponding to quarterly expirations
    expiration_rows = get_next_expiration(expiration_rows, expiration_rows.index.to_pydatetime()[0].date())

    while(not(expiration_rows.empty)):
        # Compose the precise datetime of the USA quarterly expiration
        expiration_date     = expiration_rows.index[0].date()
        expiration_datetime = pd.to_datetime(str(expiration_date) + ' ' + expiration_time, format = '%Y-%m-%d %H:%M:%S')

        # Locate the expiration row in the raw data
        expiration_index = df.index.get_loc(df.loc[expiration_datetime].name)
        
        # Data to simulate the trade are available
        if (in_window <= expiration_index):
            price_in  = df.iloc[expiration_index - in_window].open
            price_out = df.iloc[expiration_index + out_window].open
            date_in   = str(df.index[expiration_index - in_window].date())
            
            # Store outcome
            trade_return = 100 * (price_out - price_in) / price_in 
            trades_return.append(trade_return)
            trades_dates.append(date_in)

            # Log
            f_log.write(
                str(df.index[expiration_index - in_window])  + ': ' + str(price_in)  + '\n' +
                str(df.index[expiration_index + out_window]) + ': ' + str(price_out) + ' (' + str(round(trade_return, 2)) + '%)\n\n'
            )
        else:
            f_log.write(str(df.index[expiration_index - in_window]) + ': ' + 'Not enough data to simulate the trade\n\n')

        # Get all rows corresponding to quarterly expirations
        expiration_rows = get_next_expiration(expiration_rows, expiration_rows.index.to_pydatetime()[0].date())
    
    f_log.close()
    return trades_dates, trades_return

def store_sim_data(in_window, out_window, dates, returns):
    f_sim_data = open('./sim_data/' + str(in_window) + '_' + str(out_window) + '.dat', 'w')

    # Write header
    f_sim_data.write('date,return\n')
    
    # Write points to be plotted
    for date_sample, return_sample in zip(dates, np.cumsum(returns)):
        f_sim_data.write(str(date_sample)  + ',' + str(return_sample) + '\n')
    f_sim_data.close()