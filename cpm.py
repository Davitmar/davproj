#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import os, json



class CPM:
    def __init__(self, file_name):
        self.file_name = file_name

    @staticmethod
    def main(file_name, revenue_by: str):
        with open(f'{os.getcwd()}/{file_name}') as ad:
            t = csv.DictReader(ad)
            banner_rev, int_rev, rv_rev = {}, {}, {}
            banner_count, int_count, rv_count = {}, {}, {}
            for i in t:
                event = json.loads(i['event_json'])
                try:
                    unit_revenue = float(event["revenue"])
                    if i[revenue_by]:
                        if event['ad_type'] == 'banner':
                            banner_rev[(i[revenue_by])] = banner_rev.get(i[revenue_by], 0) + unit_revenue
                            banner_count[(i[revenue_by])] = banner_count.get(i[revenue_by], 0) + 1
                        elif event['ad_type'] == 'int':
                            int_rev[(i[revenue_by])] = int_rev.get(i[revenue_by], 0) + unit_revenue
                            int_count[(i[revenue_by])] = int_count.get(i[revenue_by], 0) + 1
                        elif event['ad_type'] == 'rv':
                            rv_rev[(i[revenue_by])] = rv_rev.get(i[revenue_by], 0) + unit_revenue
                            rv_count[(i[revenue_by])] = rv_count.get(i[revenue_by], 0) + 1
                except:
                    pass
        return {'banner_rev':banner_rev,'banner_count':banner_count, 'int_rev':int_rev, 'int_count':int_count, 'rv_rev':rv_rev,  'rv_count':rv_count}

#get eCPM by profile_id and ad_type
   
    def cpm_profile(self):
        banner_prof, int_prof, rv_prof = {}, {}, {}
        f = self.main(self.file_name, 'ï»¿profile_id')
        with open ('CPM_by_user.csv', 'w') as file:
            fieldnames=['ad_type', 'profile_id', 'eCPM']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for key in f['banner_rev'].keys():
                banner_prof[key] = round((f['banner_rev'])[key] / (f['banner_count'])[key] * 1000, 2)
                print(banner_prof[key])
                writer.writerow({'ad_type':'banner', 'profile_id':key, 'eCPM': banner_prof[key]})
            for key in f['int_rev'].keys():
                int_prof[key] = round((f['int_rev'])[key] / (f['int_count'])[key] * 1000, 2)
                writer.writerow({'ad_type': 'int', 'profile_id': key, 'eCPM': int_prof[key]})
            for key in f['rv_rev'].keys():
                rv_prof[key] = round((f['rv_rev'])[key] / (f['rv_count'])[key] * 1000, 2)
                writer.writerow({'ad_type': 'rv', 'profile_id': key, 'eCPM': rv_prof[key]})
        return {'banner_by_profile': banner_prof, 'int_by_profile': int_prof, 'rv_by_profile': rv_prof}

#get eCPM by ad_type - 1a.
    def cpm_by_ad_type(self):
        with open(f'{os.getcwd()}/{self.file_name}') as ad:
            t = csv.DictReader(ad)
            banner_revenue = 0
            int_revenue = 0
            rv_revenue = 0
            a = {}
            count, count_b, count_i, count_r = 0, 0, 0, 0
            for i in t:
                event = json.loads(i['event_json'])
                try:
                    unit_revenue = float(event["revenue"])
                    count += 1
                    if event['ad_type'] == 'banner':
                        count_b += 1
                        banner_revenue += unit_revenue
                    elif event['ad_type'] == 'int':
                        count_i += 1
                        int_revenue += unit_revenue
                    elif event['ad_type'] == 'rv':
                        count_r += 1
                        rv_revenue += unit_revenue
                except:
                    pass
        a['banner_CRM'] = round(banner_revenue / count_b * 1000, 2)
        a['int_CRM'] = round(int_revenue / count_i * 1000, 2)
        a['rv_CRM'] = round(rv_revenue / count_r * 1000, 2)
        return a

#get eCPM by city and ad_type - 1b.
    def city_cpm(self):
        banner_city, int_city, rv_city = {}, {}, {}
        f=self.main(self.file_name, 'city')
        with open ('CPM_by_city.csv', 'w') as file:
            fieldnames=['ad_type', 'city', 'eCPM']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for key in f['banner_rev'].keys():
                banner_city[key] = round((f['banner_rev'])[key] / (f['banner_count'])[key] * 1000, 2)
                writer.writerow({'ad_type': 'banner', 'city': key, 'eCPM': banner_city[key]})
            for key in f['int_rev'].keys():
                int_city[key] = round((f['int_rev'])[key] / (f['int_count'])[key] * 1000, 2)
                writer.writerow({'ad_type': 'int', 'city': key, 'eCPM': int_city[key]})
            for key in f['rv_rev'].keys():
                rv_city[key] = round((f['rv_rev'])[key] / (f['rv_count'])[key] * 1000, 2)
                writer.writerow({'ad_type': 'rv', 'city': key, 'eCPM': rv_city[key]})
        return {'banner_by city': banner_city, 'int_by_city': int_city, 'rv_by_city': rv_city}

#get eCPM by os_version and ad_type - 1b.
    def os_cpm(self):
        banner_os, int_os, rv_os = {}, {}, {}
        f = self.main(self.file_name, 'os_version')
        with open ('CPM_by_os.csv', 'w') as file:
            fieldnames=['ad_type', 'os_version', 'eCPM']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for key in f['banner_rev'].keys():
                banner_os[key] = round((f['banner_rev'])[key] / (f['banner_count'])[key] * 1000, 2)
                writer.writerow({'ad_type':'banner', 'os_version':key, 'eCPM': banner_os[key]})
            for key in f['int_rev'].keys():
                int_os[key] = round((f['int_rev'])[key] / (f['int_count'])[key] * 1000, 2)
                writer.writerow({'ad_type': 'int', 'os_version': key, 'eCPM': int_os[key]})
            for key in f['rv_rev'].keys():
                rv_os[key] = round((f['rv_rev'])[key] / (f['rv_count'])[key] * 1000, 2)
                writer.writerow({'ad_type': 'rv', 'os_version': key, 'eCPM': rv_os[key]})
        return {'banner_by_os': banner_os, 'int_by_os': int_os, 'rv_by_os': rv_os}

#get total revenue by city and ad_type - 1c.
    def city_total(self):
        f = self.main(self.file_name, 'city')
        for key in f['banner_rev'].keys():
            f['banner_rev'][key] = round((f['banner_rev'])[key] , 2)
        for key in f['int_rev'].keys():
            f['int_rev'][key] = round((f['int_rev'])[key] , 2)
        for key in f['rv_rev'].keys():
            f['rv_rev'][key] = round((f['rv_rev'])[key] , 2)
        return {'total_banner_city':f['banner_rev'], 'total_int_city':f['int_rev'], 'total_rv_city':f['rv_rev']}

#get total revenue by os_version and ad_type - 1c.
    def os_total(self):
        f = self.main(self.file_name, 'os_version')
        for key in f['banner_rev'].keys():
            f['banner_rev'][key] = round((f['banner_rev'])[key], 2)
        for key in f['int_rev'].keys():
            f['int_rev'][key] = round((f['int_rev'])[key], 2)
        for key in f['rv_rev'].keys():
            f['rv_rev'][key] = round((f['rv_rev'])[key], 2)
        return {'total_banner_os': f['banner_rev'], 'total_int_os': f['int_rev'], 'total_rv_os': f['rv_rev']}

#percent of revenue including city field - 4.
    def city_revenue_percent(self):
        with open(f'{os.getcwd()}/{self.file_name}') as ad:
            t = csv.DictReader(ad)
            total=0
            city_total=0
            for i in t:
                event = json.loads(i['event_json'])
                try:
                    unit_revenue = float(event["revenue"])
                    total+=unit_revenue
                    if i['city']:
                        city_total+=unit_revenue
                except:
                    pass
        percent=round(city_total/total*100,1)
        return f'{percent} % of total revenue include city field'

#get eCPM by datetime am/pm - 4.
    def time_cpm(self):
        with open(f'{os.getcwd()}/{self.file_name}') as ad:
            t = csv.DictReader(ad)
            am_rev, am_count=0, 0
            pm_rev, pm_count=0, 0
            for i in t:
                event = json.loads(i['event_json'])
                try:
                    unit_revenue = float(event["revenue"])
                    time=int((i['event_receive_datetime'])[10:13])
                    if time>=0 and time<12:
                        am_rev+=unit_revenue
                        am_count+=1
                    else:
                        pm_rev+=unit_revenue
                        pm_count+=1
                except:
                    pass
            am_cpm=round(am_rev/am_count*1000, 2)
            pm_cpm = round(pm_rev / pm_count*1000, 2)
        return {'am_cpm':am_cpm, 'pm_cpm':pm_cpm}



c = CPM('us events ad_revenue filtered 03.02-07.02.csv')

