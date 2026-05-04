import pandas as pd
from utils import execute_query     
def process_data(connection, user_input):
    result = execute_query(connection, user_input)
    if result is not None:
        df = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.description])
        return df
    else:
        return pd.DataFrame()
    
                               