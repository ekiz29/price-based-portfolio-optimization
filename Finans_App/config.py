# config.py

COLORS = {
    'plot_bg': '#1E1E1E',
    'background': '#2E2E2E',
    'text': '#FFFFFF',
    'button': '#3C3F41',
    'frame': '#2E2E2E'
}

# Senin orijinal listeni buraya koydum
TICKERS = {
        "iShares Gold Trust": "IAU","iShares Silver Trust": "SLV","S&P 500":"^GSPC","CBOE Volatility Index": "^VIX","iShares 20+ Year Treasury Bond ETF":"TLT","Bitcoin USD Price" :"BTC-USD","United States Oil Fund": "USO","Solana USD Price":"SOL-USD","Ethereum USD Price":"ETH-USD","XRP USD Price":"XRP-USD","Dogecoin USD Price" :"DOGE-USD","iShares 20+ Year Treasury Bond ETF" :"TLT","iShares MSCI Brazil ETF" :"EWZ","Vanguard International High Dividend Yield Index Fund ETF Shares" :"VYMI",
    "Abbott Laboratories": "ABT", "AbbVie": "ABBV", "Adobe": "ADBE", "Alphabet (Class A)": "GOOGL", "Alphabet (Class C)": "GOOG",
    "Amazon": "AMZN", "American Express": "AXP","Alibaba Group Holdings": "BABA", "Amgen": "AMGN","AMD (Advanced Micro Devices)":"AMD","Anheuser-Busch InBev":"BUD", "Apple": "AAPL","ARM Holdings" :"ARM","ASML Holding": "ASML",
    "Autodesk": "ADSK",	"Bank of America":"BAC","Baidu ":"BIDU", "Berkshire Hathaway B": "BRK-B", "Biogen": "BIIB", "BlackRock": "BLK", "Boeing": "BA",
    "Bristol Myers Squibb": "BMY", "Broadcom": "AVGO", "Caterpillar": "CAT", "Charles River": "CRL", "Chevron": "CVX", "Cisco": "CSCO",
    "Cloudflare": "NET", "Coca-Cola": "KO", "Conocophilips": "COP", "Costco": "COST", "CrowdStrike": "CRWD",
    "Datadog": "DDOG", "Delta Air Lines": "DAL", "Eli Lilly": "LLY", "ExxonMobil": "XOM", "Ferrari": "RACE",
    "Ford": "F", "General Electric": "GE", "General Motors": "GM", "Gilead Sciences": "GILD", "Goldman Sachs": "GS","HCA Holdings Inc":"HCA",
    "Hilton": "HLT", "Honeywell": "HON", "IBM": "IBM", "Illumina": "ILMN", "Intel": "INTC",
    "Intuit": "INTU", "JPMorgan Chase": "JPM", "Johnson & Johnson": "JNJ", "Lockheed Martin": "LMT","Live Nation Entertainment":"LYV","LVMH": "LVMUY",
    "Lyft": "LYFT", "Marriott": "MAR", "Mastercard": "MA", "McDonald's": "MCD", "Merck": "MRK","Microsoft":"MSFT",
    "Meta": "META", "Moderna": "MRNA", "Morgan Stanley": "MS","Newmont Corporation":"NEM", "Netflix": "NFLX", "Nike": "NKE",
    "Nvidia": "NVDA", "Novo Nordisk": "NVO", "Novartis": "NVS", "Okta": "OKTA", "Oracle": "ORCL",
    "Palantir": "PLTR", "Palo Alto Networks": "PANW", "PayPal": "PYPL", "Pepsi Co": "PEP", "Pfizer": "PFE",
    "Procter & Gamble": "PG", "Qualcomm": "QCOM", "Raytheon Technologies": "RTX", "Regeneron": "REGN", "Roche": "RHHBY",
    "Salesforce": "CRM", "Schlumberger": "SLB", "ServiceNow": "NOW","Shell plc":"SHEL","Shopify": "SHOP", "Snowflake": "SNOW",
    "Southwest Airlines": "LUV","Southern Copper": "SCCO", "Square (Block)": "SQ","SoFi Technologies, Inc.":"SOFI", "S&P Global": "SPGI", "Starbucks": "SBUX", "Target": "TGT", "Tesla":"TSLA",
    "Texas Instruments": "TXN", "Thermo Fisher": "TMO", "3M": "MMM", "Toyota": "TM", "Twilio": "TWLO",
    "Uber": "UBER","Unilever PLC":"UL","United Airlines": "UAL", "UnitedHealth": "UNH", "Visa": "V", "Vertex Pharmaceuticals": "VRTX",
    "Volkswagen": "VWAGY", "Walmart": "WMT", "Zscaler": "ZS",
    "Adel": "ADEL.IS", "Adese Gayrimenkul": "ADSE.GY", "Afyon Çimento": "AFYON.IS", "Akcansa": "AKCNS.IS", "Akenerji": "AKENR.IS", "Akkök": "AKKOK.IS", "Akmerkez GYO": "AKMER.IS", "Albaraka Türk": "ALBRK.IS", "Alarko Carrier": "ALCAR.IS", "Alarko Holding": "ALARK.IS", "Alcatel Lucent": "ALTHD.IS", "Alcı Yatırım": "ALCYT.IS", "Aksu Enerji ve Ticaret": "AKSUE.IS", "Anadolu Efes Malt": "AEFES.IS", "Anadolu Sigorta": "ANSUR.IS", "Anel Elektrik": "ANELE.IS", "Arçelik": "ARCLK.IS", "Aselsan": "ASELS.IS", "Aygaz": "AYGAZ.IS", "Batikim": "BATIK.IS", "Borusan Birleşik": "BORUB.IS", "Borusan Yatırım": "BRYAT.IS", "BİM Mağazalar": "BIMAS.IS", "Coca-Cola İçecek": "CCOLA.IS", "Deva Holding": "DEVA.IS","Dogan Sirketler Grubu Holding A.S.":"DOHOL.IS", "Doğuş Otomotiv": "DOAS.IS", "Ege Endüstri": "EGEEN.IS", "Enka İnşaat": "ENKAI.IS", "Erdemir": "EREGL.IS", "Ford Otosan": "FROTO.IS", "Garanti BBVA": "GARAN.IS","Galata Wind Enerji A.S.":"GWIND.IS","Hektaş": "HEKTS.IS", "ICBC Turkey": "ICBCT.IS", "Kardemir (D)": "KRDMD.IS", "Karel": "KAREL.IS", "Koç Holding": "KCHOL.IS", "Logo Yazılım": "LOGO.IS", "Mavi Giyim": "MAVI.IS", "Migros Ticaret": "MGROS.IS", "Netas Telekom": "NETAS.IS", "Otokar": "OTKAR.IS", "Oyak Çimento": "OYAKC.IS", "Pegasus": "PGSUS.IS", "Petkim": "PETKM.IS", "Sabancı Holding": "SAHOL.IS", "Sasa Polyester": "SASA.IS", "Şişecam": "SISE.IS", "TAV Havalimanları": "TAVHL.IS", "Tekfen Holding": "TKFEN.IS", "Teknosa": "TKNSA.IS", "TSKB": "TSKB.IS", "Tümosan": "TMSN.IS", "Tüpraş": "TUPRS.IS", "Türk Hava Yolları": "THYAO.IS", "Türk Telekom": "TTKOM.IS", "Turkcell": "TCELL.IS", "Türkiye Halk Bankası": "HALKB.IS", "Türkiye İş Bankası (C)": "ISCTR.IS", "Türkiye Sigorta": "TURSG.IS", "Ülker Bisküvi": "ULKER.IS", "VakıfBank": "VAKBN.IS", "Vestel": "VESTL.IS","Tofas Türk Otomobil Fabrikasi Anonim Sirketi":"TOASO.IS", "Yapı ve Kredi Bankası": "YKBNK.IS", "Yataş": "YATAS.IS", "Zorlu Enerji": "ZOREN.IS"
    # Not: Buraya senin orijinal proje.py dosyasındaki tüm uzun listeyi yapıştırabilirsin.
}