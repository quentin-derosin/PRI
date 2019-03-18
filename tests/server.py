import pandas as pd
import pycountry
from pytrends.request import TrendReq
from collections import OrderedDict


class utilGraph:
    def __init__(self, index, value):
        self.index = index
        self.value = value


class Server:

    def forCountry(country, product):
        pytrend = TrendReq()
        ctemp = pycountry.countries.get(name=country.title())
        if ctemp is None:
            return None
        print(country.title())
        pytrend.build_payload(kw_list=[product], geo=ctemp.alpha_2)
        interest_by_region_df = pytrend.interest_by_region(resolution='REGION')

        dc = interest_by_region_df.loc[(interest_by_region_df != 0).any(axis=1)]
        column_name = dc.columns.values
        dc = dc.sort_values(by=column_name[0], ascending=False).iloc[0:10]

        return dc

    def getRelatedTopic(product):
        pytrend = TrendReq()
        pytrend.build_payload(kw_list=[product])

        related_topics = pytrend.related_topics()
        related_queries = pytrend.related_queries()

        list_of_related_queries = []
        list_of_related_topics = []

        for k in related_queries:
            rel_qarray = related_queries[k]['top']

        if rel_qarray is not None:
            related_queries2 = rel_qarray.loc[:, 'query']
            df = pd.DataFrame(related_queries2, columns=['query'])
            for index, row in df.iterrows():
                list_of_related_queries.append(row["query"])

            for k in related_topics:
                if related_topics[k]['title'] is not None:
                    related_tarray = related_topics[k]['title']

            list_of_related_topics = related_tarray.values.tolist()

            if len(list_of_related_topics) > len(list_of_related_queries):
                list_of_related_topics = list_of_related_topics[0:len(list_of_related_queries) - 1]
            elif len(list_of_related_topics) < len(list_of_related_queries):
                list_of_related_queries = list_of_related_queries[0:len(list_of_related_topics) - 1]

            return pd.DataFrame(OrderedDict([
                ('related_query', list_of_related_queries),
                ('related_topic', list_of_related_topics),
            ]))


    def forCountryMarketing(Country):
        pytrend = TrendReq()
        list_analog_name = ['Email marketing', 'Radio Advertising', 'Mobile Marketing', 'Television Advertising',
                            'Facebook Advertisement']
        list_digital_name = ['Newspaper Marketing', 'Billboards', 'Bus Shelter Ads', 'Print Ads', 'Fliers']
        ctemp = pycountry.countries.get(name=Country.title())
        pytrend.build_payload(kw_list=list_analog_name, geo=ctemp.alpha_2)  # It can take maximum 5 products in kw_list
        digital_marketing = pytrend.interest_by_region(resolution='REGION')
        pytrend.build_payload(kw_list=list_digital_name, geo=ctemp.alpha_2)
        analog_marketing = pytrend.interest_by_region(resolution='REGION')

        list_analog_data = [
            analog_marketing['Newspaper Marketing'].mean(),
            analog_marketing['Billboards'].mean(),
            analog_marketing['Bus Shelter Ads'].mean(),
            analog_marketing['Print Ads'].mean(),
            analog_marketing['Fliers'].mean()
        ]

        list_digital_data = [
            digital_marketing['Email marketing'].mean(),
            digital_marketing['Radio Advertising'].mean(),
            digital_marketing['Mobile Marketing'].mean(),
            digital_marketing['Television Advertising'].mean(),
            digital_marketing['Facebook Advertisement'].mean(),
        ]

        digital = utilGraph(list_digital_name, list_digital_data)
        analog = utilGraph(list_analog_name, list_analog_data)
        return digital, analog
