

import pandas as pd
import pycountry
from pytrends.request import TrendReq


class Server:

   #User enters the country value
    # somehow find a way to map the name of the country to country codes


    def forCountry(Country, product):
        print("Product : " + product)
        print("Country : " + Country.title())
        pytrend = TrendReq()
        ctemp=pycountry.countries.get(name=Country.title())
        pytrend.build_payload(kw_list=[product], geo=ctemp.alpha_2)
        interest_by_region_df = pytrend.interest_by_region(resolution='REGION')
        related_topics = pytrend.related_topics()
        related_queries = pytrend.related_queries()
        interest_overTime = pytrend.interest_over_time()
        dc = interest_by_region_df.loc[(interest_by_region_df != 0).any(axis=1)]
        column_name = dc.columns.values
        dc = dc.sort_values(by=column_name[0],ascending= False).iloc[0:10]
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

        return dc, list_of_related_queries, list_of_related_topics

    def forCountryMarketing(Country):
        pytrend = TrendReq()
        ctemp = pycountry.countries.get(name=Country.title())
        pytrend.build_payload(kw_list=['Email marketing', 'Radio Advertising', 'Mobile Marketing', 'Television Advertising', 'Facebook Advertisement'], geo=ctemp.alpha_2) #It can take maximum 5 products in kw_list
        digital_marketing = pytrend.interest_by_region(resolution='REGION')
        pytrend.build_payload(kw_list=['Newspaper Marketing', 'Billboards', 'Bus Shelter Ads', 'Print Ads','Fliers'],geo=ctemp.alpha_2)
        analog_marketing = pytrend.interest_by_region(resolution='REGION')

        return digital_marketing , analog_marketing


    def RecommendationText(count,analog,digital):
        recommedantion = ''

        maxAnag = 0
        Anag_Name= ''
        typeofAnalog=0
        Digi_Name=''
        maxDigi = 0
        typeofDigital=0
        for marketing in analog:
           if(marketing>maxAnag):
               maxAnag=marketing
               typeofAnalog= analog.index(marketing);
               if typeofAnalog == 0 :
                   Anag_Name= 'Newspaper Marketing'
               elif typeofAnalog == 1:
                   Anag_Name = 'Billboards'
               elif typeofAnalog == 2:
                   Anag_Name = 'Bus Shelter Ads'
               elif typeofAnalog == 1:
                   Anag_Name = 'Print Ads'
               elif typeofAnalog == 1:
                   Anag_Name = 'Fliers'


        for marketing in digital:
           if(marketing>maxDigi):
               maxDigi=marketing
               typeofDigital = digital.index(marketing)
               if typeofDigital == 0 :
                   Digi_Name= 'Email marketing'
               elif typeofAnalog == 1:
                   Digi_Name = 'Radio Advertising'
               elif typeofAnalog == 2:
                   Digi_Name = 'Mobile Marketing'
               elif typeofAnalog == 1:
                   Digi_Name = 'Television Advertising'
               elif typeofAnalog == 1:
                   Digi_Name = 'Facebook Advertisement'


        if maxDigi > maxAnag:
            recommedantion =  'Thes most popular analog marketing in ' + count + ' is ' + Anag_Name  +' and the most popular digital marketing is ' + Digi_Name + '.\n' + \
                              'As the results show the most recommended approach of marketing is the Digital marketing approach'
        else:
            recommedantion = 'Thes most popular analog marketing in ' + count + ' is ' + Anag_Name + 'and the most popular digital marketing is ' + Digi_Name + '.\n' + \
                             'As the results show the most recommended approach of marketing is the Analog marketing approach'

        print(recommedantion)


        return recommedantion
