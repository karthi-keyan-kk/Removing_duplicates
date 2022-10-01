import pandas as pd
from collections import Counter
import pygsheets

gc = pygsheets.authorize(service_file="data-science-363622-821c1039e981.json")

data = pd.read_csv("Sample data for assignment.csv")
data.dropna()

# print(data)

hscodes_list = []
product_list = []
quantity_list = []
unit_list = []
unit_rate_list = []
currency_list = []
total_usd_list = []

hscode_data = data["HS_CODE"]
duplicated_data = data[hscode_data.isin(hscode_data[hscode_data.duplicated()])].sort_values("HS_CODE")
duplicated_data_hscode_to_total_usd = duplicated_data.iloc[:, 1:8]

# print(duplicated_data_hscode_to_total_usd)

hs_code = duplicated_data_hscode_to_total_usd["HS_CODE"]
products = duplicated_data_hscode_to_total_usd["PRODUCT"]
quantities = duplicated_data_hscode_to_total_usd["QUANTITY"]
units = duplicated_data_hscode_to_total_usd["UNIT"]
unit_rates = duplicated_data_hscode_to_total_usd["UNIT_RATE"]
currencies = duplicated_data_hscode_to_total_usd["CURRENCY"]
total_usd = duplicated_data_hscode_to_total_usd["TOTAL_USD"]

for hscode in hs_code:
    hscodes_list.append(hscode)
# print(hscodes_list)

d = Counter(hscodes_list)
# print(d)

for product in products:
    product_list.append(product)

for quantity in quantities:
    quantity_list.append(quantity)

for unit in units:
    unit_list.append(unit)

for unit_rate in unit_rates:
    unit_rate_list.append(unit_rate)

for currency in currencies:
    currency_list.append(currency)

for usd in total_usd:
    total_usd_list.append(usd)

vals = 3   # [2, 3, 5, 6, 10, 11, 16, 21]
keys_list = []
hscode_index_list = []

for keys, values in d.items():
    # for val in vals:
    if vals == values:
        keys_list.append(keys)

# print(keys_list)
# position = keys_list

for hscode_index in range(len(hscodes_list)):
    # print(hscode_index)
    # for key_list in keys_list:
    # print(key_list)
    if hscodes_list[hscode_index] == keys_list[0]:
        # print(hscodes_list[hscode_index])
        hscode_index_list.append(hscode_index)

# print(hscode_index_list)
product_name = []
product_quantity = []
product_unit = []
product_unit_rate = []
product_currency = []
product_USD = []
sstr_dict = {}

for index in hscode_index_list:
    # print(index)
    product_name.append(product_list[index])
    product_quantity.append(quantity_list[index])
    product_unit.append(unit_list[index])
    product_unit_rate.append(unit_rate_list[index])
    product_currency.append(currency_list[index])
    product_USD.append(total_usd_list[index])

    sstr_dict = {
        "Hs Code": keys_list[0],
        "Product Name": product_name,
        "Quantity": product_quantity,
        "Unit": product_unit,
        "Unit Rate": product_unit_rate,
        "Currency": product_currency,
        "Total USD": product_USD,
    }

# print(sstr)
#
# print(sstr_dict)

# for keys, values in sstr_dict.items():

Data = pd.DataFrame(sstr_dict)
Data.to_csv("Duplicated_data.csv", index=False, mode="a")

sheet = gc.open("Data")

wks = sheet[0]

wks.set_dataframe(Data, (1, 1))
