from typing import Optional
from fastapi import FastAPI, Query
from fastapi.exceptions import RequestValidationError

import pandas as pd
import ast
import psData

app = FastAPI()

# Perform psData operations to get PS data
ps_data = psData.get_process_stats()
ps_list = psData.parse_process_stats(ps_data)
ps_df = psData.store_process_stats(ps_list)


def filter_processes(ps_df : pd.DataFrame, user_query : str) -> pd.DataFrame:
    """Filters processes according to user query from url
   
    Returns
    -------
    pd.DataFrame
        pandas dataframe containing the filtered data
    """
    user_query = user_query.strip('\'')
    result_df = ps_df.query(user_query)
    return result_df
   
def sort_processes(ps_df : pd.DataFrame, user_sort : list) -> pd.DataFrame:
    """Sorts processes according to user sort list from url
   
    Returns
    -------
    pd.DataFrame
        pandas dataframe containing the sorted data
    """
    result_df = ps_df.sort_values(by=user_sort, ascending=True)
    return result_df
   
   
@app.get("/")
def process_root() -> dict:
    """Base url, with no filters/sorting, strictly data
   
    Returns
    -------
    dict
        dictionary containing all the process data
    """
    result = ps_df.to_json(orient='records')
    result = ast.literal_eval(result)
    return {"Processes" : result}
   
@app.get("/filter/")
def process_filter(q : str = Query(..., max_length=50), s : Optional[str] = Query(None, max_length=100)) -> dict:   
    """ Filter url, takes in query string and [optional] sorting list from user URL
    First will filter data, then perform any optional sorting on filtered data
    Returns
    -------
    dict
        dictionary containing the filtered and [optional] sorted process data
    """
    result_df = filter_processes(ps_df, q)
    if s is not None:
        sort_list = ast.literal_eval(s)
        result_df = sort_processes(result_df, sort_list)
      
    result = result_df.to_json(orient='records')
    result = ast.literal_eval(result)
    
    return {"Processes" : result}
   
@app.get("/sort/")
def process_sort(s : str = Query(..., max_length=100)) -> dict:
    """Sort url, takes in sorting list from user URL
    Sorts the data according to sorting list
    Returns
    -------
    dict
        dictionary containing all the sorted process data
    """
    sort_list = ast.literal_eval(s)
    result_df = sort_processes(ps_df, sort_list)
    
    result = result_df.to_json(orient='records')
    result = ast.literal_eval(result)
    
    return {"Processes" : result}
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse("Invalid query")
    
