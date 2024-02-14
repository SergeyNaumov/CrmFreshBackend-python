def get_query_search_tables():
    return [
          {'t':'arbitrage_case','a':'wt'},
          {'t':'arbitrage_case_type','a':'t','l':'wt.type_id=t.id'},
          {'t':'arbitrage_court','a':'c','l':'wt.court_id=c.id'},
          {'t':'arbitrage_case_plaintiff', 'a':'pl','l':'wt.id=pl.case_id'}, # истец
          {'t':'arbitrage_case_respondent', 'a':'resp','l':'wt.id=resp.case_id'}, # ответчик
    ]