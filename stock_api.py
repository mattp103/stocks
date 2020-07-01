import requests
import json
import re

company_codes = {'AAL.L': 'ANGLO AMERICAN', 'JMAT.L': 'JOHNSON MATTHEY PLC', 'ABF.L': 'ASSOCIAT BRIT FOODS', 'KAZ.L': 'KAZAKHMYS', 'ADM.L': 'ADMIRAL GROUP', 'KGF.L': 'KINGFISHER', 'ADN.L': 'ABERDEEN ASSET MGMT', 'LAND.L': 'LAND SEC R.E.I.T.', 'AGK.L': 'AGGREKO', 'LGEN.L': 'LEGAL & GENERAL', 'AMEC.L': 'AMEC', 'LLOY.L': 'LLOYDS BANKING GRP', 'ANTO.L': 'ANTOFAGASTA', 'MGGT.L': 'MEGGITT', 'ARM.L': 'ARM HOLDINGS', 'MKS.L': 'MARKS & SPENCER', 'ASHM.L': 'ASHMORE GRP', 'MRW.L': 'MORRISON SUPERMKTS', 'AV.L': 'AVIVA', 'NG.L': 'NATIONAL GRID', 'AZN.L': 'ASTRAZENECA', 'NXT.L': 'NEXT', 'BA.L': 'BAE SYSTEMS', 'OML.L': 'OLD MUTUAL', 'BARC.L': 'BARCLAYS', 'PFC.L': 'PETROFAC', 'BATS.L': 'BRIT AMER TOBACCO', 'POLY.L': 'POLYMETAL INTL', 'BG.L': 'BG GROUP', 'PRU.L': 'PRUDENTIAL', 'BLND.L': 'BRIT LAND CO REIT', 'PSON.L': 'PEARSON', 'BLT.L': 'BHP BILLITON', 'RB.L': 'RECKITT BENCK GRP', 'BNZL.L': 'BUNZL', 'RBS.L': 'ROYAL BK SCOTL GR', 'BP.L': 'BP', 'RDSB.L': 'ROYAL DUTCH SHELL-B', 'BRBY.L': 'BURBERRY GROUP', 'REL.L': 'REED ELSEVIER PLC', 'BSY.L': 'B SKY B GROUP', 'REX.L': 'REXAM', 'BT-A.L': 'BT GROUP', 'RIO.L': 'RIO TINTO', 'CCL.L': 'CARNIVAL', 'RR.L': 'ROLLS-ROYCE HLDGS', 'CNA.L': 'CENTRICA', 'RRS.L': 'RANDGOLD RESOURCES', 'CPG.L': 'COMPASS GROUP', 'RSA.L': 'RSA INSUR GRP', 'CPI.L': 'CAPITA', 'RSL.L': 'RESOLUTION NPV', 'CRDA.L': 'CRODA INTL PLC', 'SAB.L': 'SABMILLER', 'CRH.L': 'CRH PLC', 'SBRY.L': 'SAINSBURY', 'CSCG.L': 'CAP SHOP CENTRES', 'SDR.L': 'SCHRODERS', 'DGE.L': 'DIAGEO', 'SDRC.L': 'SCHRODERS NVTG', 'EMG.L': 'MAN GROUP', 'SGE.L': 'SAGE GRP', 'ENRC.L': 'EURASIAN NATURAL', 'SHP.L': 'SHIRE', 'EVR.L': 'EVRAZ', 'SL.L': 'STANDARD LIFE', 'EXPN.L': 'EXPERIAN', 'SMIN.L': 'SMITHS GROUP', 'FRES.L': 'FRESNILLO', 'SN.L': 'SMITH & NEPHEW', 'GFS.L': 'G4S', 'SRP.L': 'SERCO GROUP', 'GKN.L': 'GKN', 'SSE.L': 'SSE', 'GLEN.L': 'GLENCORE INTL', 'STAN.L': 'STANDARD CHARTERED', 'GSK.L': 'GLAXOSMITHKLINE', 'SVT.L': 'SEVERN TRENT', 'HL.L': 'HARGREAVES LANS', 'TATE.L': 'TATE & LYLE', 'HMSO.L': 'HAMMERSON REIT', 'TLW.L': 'TULLOW OIL', 'HSBA.L': 'HSBC HLDG', 'TSCO.L': 'TESCO PLC', 'IAG.L': 'INTL. CONS. AIR GRP', 'ULVR.L': 'UNILEVER', 'IAP.L': 'ICAP', 'UU.L': 'UNITED UTILITIES GR', 'IHG.L': 'INTERCONT HOTELS', 'VED.L': 'VEDANTA RESOURCES', 'IMI.L': 'IMI PLC', 'VOD.L': 'VODAFONE GRP', 'IMT.L': 'IMPERIAL TOBACCO', 'WEIR.L': 'WEIR GROUP', 'IPR.L': 'INTERNATIONAL POWER', 'WOS.L': 'WOLSELEY', 'ITRK.L': 'INTERTEK GROUP', 'WPP.L': 'WPP', 'ITV.L': 'ITV', 'WTB.L': 'WHITBREAD', 'XTA.L': 'XSTRATA'}
company_ids = dict(zip(company_codes.keys(), range(1, len(company_codes.keys())+1)))


def get_all_current_data():
    url = "https://spreadsheets.google.com/feeds/list/0AhySzEddwIC1dEtpWF9hQUhCWURZNEViUmpUeVgwdGc/1/public/basic?alt=json"

    # get json api_data and converts to dict
    decoded_json = json.loads(requests.get(url).text)

    companies_data = {}
    codes = {value: key for key, value in company_codes.items()}

    # go through each company in the decoded json and gets the name, change and price and adds it to "companies_data"
    for company in decoded_json["feed"]["entry"]:
        data = re.split(': |, ', company["content"]['$t'])  # turns each key and val into items in list "data"
        # join together key and value pairs in the list to form dict with key: company name and value: dict of data
        companies_data[codes[data[1]]] = {data[i]: data[i + 1] for i in range(0, len(data), 2)}

    return companies_data


def get_company_current_data(code):
    url = "https://spreadsheets.google.com/feeds/list/0AhySzEddwIC1dEtpWF9hQUhCWURZNEViUmpUeVgwdGc/1/public/basic?alt=json&sq=symbol=" + code
    decoded_json = json.loads(requests.get(url).text)

    data = re.split(': |, ', decoded_json["feed"]["entry"][0]['content']['$t'])

    return {data[i]: data[i + 1] for i in range(0, len(data), 2)}


if __name__ == "__main__":
    print(get_all_current_data())
    print(get_company_current_data("AAL.L"))
    print(company_ids)
