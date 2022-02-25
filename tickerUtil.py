
def getTop100Tickers():

    top_100_csv_str = "AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA,TSM,FB,V,UNH,JPM,JNJ,BAC,WMT,PG,MA,HD,ZOM,BABA,DIS,ASML,KO,CVX,PFE,ABBV,TM,NTES,AVGO,LLY,CSCO,PEP,NVO,COST,VZ,ADBE,NKE,TMO,ABT,CMCSA,WFC,CRM,ACN,ORCL,SHEL,DHR,NVS,INTC,QCOM,MRK,MCD,UPS,AZN,NFLX,T,MS,BHP,PM,TXN,SCHW,TMUS,UNP,RY,NEE,BMY,LIN,TD,LOW,AXP,HSBC,INTU,RTX,MDT,TTE,CVS,SAP,SNY,SONY,UL,HON,PYPL,AMGN,RIO,C,CHTR,HDB,AMAT,BA,NOW,COP,GS,DEO,BLK,JD,IBM,BUD,LMT,ANTM,PLD"
    tickers = top_100_csv_str.split(",")
    return tickers

def getInterestingTickersNotTop100():
    tickers = []
    tickers += ["COIN","PLTR","EA","GE","AAL","TAP","YUM","WM","GM","CRWD"]
    return tickers

if __name__ == "__main__":
    top100Tickers = getTop100Tickers()
    print(top100Tickers)