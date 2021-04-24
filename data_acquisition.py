import pandas as pd

def read_input_data(stock_index, remove_NaNs):
    raw_data = pd.read_csv('../input_data/' + stock_index + '/m30.csv',
                           parse_dates = [['<DTYYYYMMDD>', '<TIME>']])

    # --------------------------
    # -- Drop useless columns --
    # --------------------------
    raw_data = raw_data.drop(['<TICKER>'],  axis = 'columns')
    raw_data = raw_data.drop(['<PER>'],     axis = 'columns')
    raw_data = raw_data.drop(['<VOL>'],     axis = 'columns')
    raw_data = raw_data.drop(['<OPENINT>'], axis = 'columns')

    # --------------------
    # -- Rename columns --
    # --------------------
    raw_data.rename({'<DTYYYYMMDD>_<TIME>': 'date',
                     '<OPEN>'             : 'open',
                     '<HIGH>'             : 'high',
                     '<LOW>'              : 'low',
                     '<CLOSE>'            : 'close',},
                     axis = 'columns', inplace = True)

    #- -------------------------------------------------
    # -- Add day name to identify the expiration days --
    #- -------------------------------------------------
    raw_data['day_of_week'] = raw_data['date'].dt.day_name()

    raw_data.set_index(keys              = 'date', 
                       inplace          = True,
                       verify_integrity = True,)

    if remove_NaNs == True:
        raw_data = raw_data.dropna()
    
    return raw_data