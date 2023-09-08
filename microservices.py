import json
import requests
from datetime import date

f = open('data_file.json')
data = json.load(f)

#exchange_lst = []
exchange_lst = [{'result': 'success', 'documentation': 'https://www.exchangerate-api.com/docs', 'terms_of_use': 'https://www.exchangerate-api.com/terms', 'time_last_update_unix': 1694044801, 'time_last_update_utc': 'Thu, 07 Sep 2023 00:00:01 +0000', 'time_next_update_unix': 1694131201, 'time_next_update_utc': 'Fri, 08 Sep 2023 00:00:01 +0000', 'base_code': 'USD', 'conversion_rates': {'USD': 1, 'AED': 3.6725, 'AFN': 73.6583, 'ALL': 100.5806, 'AMD': 385.8786, 'ANG': 1.79, 'AOA': 835.1573, 'ARS': 350.0, 'AUD': 1.5666, 'AWG': 1.79, 'AZN': 1.7, 'BAM': 1.8236, 'BBD': 2.0, 'BDT': 109.7269, 'BGN': 1.8236, 'BHD': 0.376, 'BIF': 2827.0724, 'BMD': 1.0, 'BND': 1.363, 'BOB': 6.9288, 'BRL': 4.9737, 'BSD': 1.0, 'BTN': 83.1945, 'BWP': 13.7423, 'BYN': 3.0243, 'BZD': 2.0, 'CAD': 1.3645, 'CDF': 2389.7231, 'CHF': 0.8913, 'CLP': 873.7709, 'CNY': 7.3157, 'COP': 4094.7877, 'CRC': 536.3631, 'CUP': 24.0, 'CVE': 102.8126, 'CZK': 22.5939, 'DJF': 177.721, 'DKK': 6.9551, 'DOP': 56.7239, 'DZD': 137.0032, 'EGP': 30.9082, 
'ERN': 15.0, 'ETB': 55.3344, 'EUR': 0.9325, 'FJD': 2.2741, 'FKP': 0.7992, 'FOK': 6.9562, 'GBP': 0.7993, 'GEL': 2.6242, 'GGP': 0.7992, 'GHS': 11.4039, 'GIP': 0.7992, 'GMD': 64.1017, 'GNF': 8581.1498, 'GTQ': 7.8692, 'GYD': 209.2282, 'HKD': 7.843, 'HNL': 24.6826, 'HRK': 7.0253, 'HTG': 136.509, 'HUF': 362.8622, 'IDR': 15315.5666, 'ILS': 3.8289, 'IMP': 0.7992, 'INR': 83.2091, 'IQD': 1310.7981, 'IRR': 41947.4373, 'ISK': 133.8168, 'JEP': 0.7992, 'JMD': 154.6584, 'JOD': 0.709, 'JPY': 147.5614, 'KES': 146.1916, 'KGS': 88.1723, 'KHR': 4159.1704, 'KID': 1.5666, 'KMF': 458.7173, 'KRW': 1333.5242, 'KWD': 0.3085, 'KYD': 0.8333, 'KZT': 463.3102, 'LAK': 19450.0588, 'LBP': 15000.0, 'LKR': 321.1326, 'LRD': 189.5071, 'LSL': 19.2219, 'LYD': 4.8432, 'MAD': 10.1804, 'MDL': 17.8712, 'MGA': 4515.075, 'MKD': 57.3598, 'MMK': 2099.3403, 'MNT': 3498.5751, 'MOP': 8.0778, 'MRU': 38.4881, 'MUR': 45.1958, 'MVR': 15.4308, 'MWK': 1074.4247, 'MXN': 17.5767, 'MYR': 4.6734, 'MZN': 63.8827, 'NAD': 19.2219, 'NGN': 757.9205, 'NIO': 36.5653, 'NOK': 10.7131, 'NPR': 133.1112, 'NZD': 1.7019, 'OMR': 0.3845, 'PAB': 1.0, 'PEN': 3.7016, 'PGK': 3.6326, 'PHP': 57.0294, 'PKR': 307.6766, 'PLN': 4.2325, 'PYG': 7242.4808, 
'QAR': 3.64, 'RON': 4.6182, 'RSD': 109.1208, 'RUB': 97.9749, 'RWF': 1214.2686, 'SAR': 3.75, 'SBD': 8.506, 'SCR': 13.2868, 'SDG': 561.1686, 'SEK': 11.1095, 'SGD': 1.3631, 'SHP': 0.7992, 'SLE': 21.8981, 'SLL': 21898.1274, 'SOS': 569.333, 'SRD': 38.1441, 'SSP': 1004.9802, 'STN': 22.8441, 'SYP': 12962.6009, 'SZL': 19.2219, 'THB': 35.5321, 'TJS': 10.9447, 'TMT': 3.4977, 'TND': 3.126, 'TOP': 2.363, 
'TRY': 26.8314, 'TTD': 6.757, 'TVD': 1.5666, 'TWD': 31.9492, 'TZS': 2506.1425, 'UAH': 36.9342, 'UGX': 3727.348, 'UYU': 37.7254, 'UZS': 12104.2067, 'VES': 33.1115, 'VND': 24035.643, 'VUV': 122.0483, 
'WST': 2.7765, 'XAF': 611.623, 'XCD': 2.7, 'XDR': 0.7558, 'XOF': 611.623, 'XPF': 111.2667, 'YER': 250.2035, 'ZAR': 19.224, 'ZMW': 20.5666, 'ZWL': 4650.7373}}]

def get_privacy_list():
    privacy_list = data['person_array']
    return privacy_list

def get_token():
    token = data['telegram_token']
    return token

def request_rate():
    # Where USD is the base currency you want to use
    url = data['exchange_url']
    
    # Making our request
    response = requests.get(url)
    exchange_data = response.json()
    exchange_lst.append(exchange_data)
    return

def get_rate(currency):
    rate = exchange_lst[0]['conversion_rates'][currency]
    return rate

def get_date():
    today = date.today()
    date_lst = [today.day,today.month,today.year]
    return date_lst