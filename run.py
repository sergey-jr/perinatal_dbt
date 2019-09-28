import pandas as pd
import numpy as np
import json
import os
from pymongo import MongoClient
import pprint

cwd = os.getcwd()
files = {"2016": [], "2017": [], "2018": []}
regions = ['Российская Федерация', 'Центральный федеральный округ', 'Белгородская область', 'Брянская область',
           'Владимирская область', 'Воронежская область', 'Ивановская область', 'Калужская область',
           'Костромская область', 'Курская область', 'Липецкая область', 'Московская область', 'Орловская область',
           'Рязанская область', 'Смоленская область', 'Тамбовская область', 'Тверская область', 'Тульская область',
           'Ярославская область', 'г.Москва', 'Северо-Западный федеральный округ', 'Республика Карелия',
           'Республика Коми', 'Архангельская область', 'Hенецкий авт.округ', 'Архангельская область без автономии',
           'Вологодская область', 'Калининградская область', 'Ленинградская область', 'Мурманская область',
           'Новгородская область', 'Псковская область', 'г.Санкт-Петербург', 'Южный федеральный округ',
           'Республика Адыгея', 'Республика Калмыкия', 'Краснодарский край', 'Астраханская область',
           'Волгоградская область', 'Ростовская область', 'Северо-Кавказский федеральный округ', 'Республика Дагестан',
           'Республика Ингушетия', 'Кабардино-Балкарская Республика', 'Карачаево-Черкесская Республика',
           'Республика Северная Осетия- Алания', 'Чеченская Республика', 'Ставропольский край',
           'Приволжский федеральный округ', 'Республика Башкортостан', 'Республика Марий Эл', 'Республика Мордовия',
           'Республика Татарстан(Татарстан)', 'Удмуртская Республика', 'Чувашская Республика(Чувашия)', 'Пермский край',
           'Кировская область', 'Hижегородская область', 'Оренбургская область', 'Пензенская область',
           'Самарская область', 'Саратовская область', 'Ульяновская область', 'Уральский федеральный округ',
           'Курганская область', 'Свердловская область', 'Тюменская область', 'Ханты-Мансийский авт.округ-Югра',
           'Ямало-Hенецкий авт.округ', 'Тюменская область без автономии', 'Челябинская область',
           'Сибирский федеральный округ', 'Республика Алтай', 'Республика Бурятия', 'Республика Тыва',
           'Республика Хакасия', 'Алтайский край', 'Забайкальский край', 'Красноярский край', 'Иркутская область',
           'Кемеровская область', 'Новосибирская область', 'Омская область', 'Томская область',
           'Дальневосточный федеральный округ', 'Республика Саха (Якутия)', 'Камчатский край', 'Приморский край',
           'Хабаровский край', 'Амурская область', 'Магаданская область', 'Сахалинская область',
           'Еврейская автономная область', 'Чукотский авт.округ', 'Крымский федеральный округ', 'Республика Крым',
           'г Севастополь']
# client = MongoClient("mongodb://mongo_root:mongo_root@cluster0-shard-00-00-lvewy.mongodb.net:27017,"
#                      "cluster0-shard-00-01-lvewy.mongodb.net:27017,cluster0-shard-00-02-lvewy."
#                      "mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&"
#                      "retryWrites=true&w=majority")
# db = client.perinatal
# table = db.statiscs
for r, d, f in os.walk(cwd):
    for file in f:
        if '.xls' in file and '~' not in file:
            path = os.path.join(r, file)
            if "2016" in r:
                files["2016"].append(path)
            elif "2017" in r:
                files["2017"].append(path)
            else:
                files["2018"].append(path)
for year in files:
    for i, file_path in enumerate(files[year]):
        print()
        print(file_path)
        df = pd.read_excel(file_path, sheet_name='t1_1')
        df.columns = ['region', 'birth', 'd1', 'd2', 'd3', 'death', 'd4', 'd5', 'd6', 'death_children', 'd7', 'd8',
                      'd9', 'inc_decr', 'd10', 'marriage', 'd11', 'd12', 'd13', 'divorce', 'd14', 'd15', 'd16']
        df = df[df.region.isin(regions)]
        df = df[['region', 'birth', 'death', 'death_children', 'inc_decr', 'marriage', 'divorce']]
        df.insert(7, "year", year)
        month = f'0{i + 1}' if i < 9 else str(i + 1)
        df.insert(8, "month", month)
        file = open(f'data/{year}/{month}.csv', mode='w')
        file.close()
        df.to_csv(f'data/{year}/{month}.csv')
        # records = list(json.loads(df.T.to_json()).values())
        # table.insert_many(records)

# res_year = table.find(projection={"year": 1}).distinct("year")
# year = [str(post) for post in res_year]
# res_month = table.find(projection={"month": 1}).distinct("month")
# month = [str(post) for post in res_month]
# res_region = table.find(projection={"region": 1}).distinct("region")
# region = [str(post) for post in res_region]
# print(year)
# print(month)
# print(len(region), region)
