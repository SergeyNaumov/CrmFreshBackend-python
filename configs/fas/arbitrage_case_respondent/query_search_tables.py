def get_query_search_tables():
    return [
          {'t':'arbitrage_case_respondent','a':'wt'},
          {'t':'arbitrage_egrul','a':'e','l':'e.id=wt.egrul_id','lj':0},
          {'t':'arbitrage_case','a':'c','l':'wt.case_id=c.id'},
          {'t':'arbitrage_court','a':'court','l':'c.court_id=court.id'},
          {'t':'arbitrage_egrul_email','a':'email','l':'email.egrul_id=e.id'},
          {'t':'arbitrage_egrul_phone','a':'phone','l':'phone.egrul_id=e.id'},
          {'t':'arbitrage_case_plaintiff', 'a':'pl','l':'c.id=pl.case_id'}, # истец
          {'t':'arbitrage_egrul_finans', 'a':'fin','l':'fin.egrul_id=e.id'}, # финансы
    ]






