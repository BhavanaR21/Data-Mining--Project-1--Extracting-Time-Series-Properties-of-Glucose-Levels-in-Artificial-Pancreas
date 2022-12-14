#45
import pandas as pd

df_cgm = pd.read_csv("CGMData.csv")
df_insulin = pd.read_csv("InsulinData.csv")



date, time = df_insulin[df_insulin.Alarm.str.startswith("AUTO MODE ACTIVE PLGM OFF", na=False)].iloc[1][['Date', 'Time']]
timestamp = pd.to_datetime(date + ' ' + time)

df_cgm['tstamp'] = pd.to_datetime(df_cgm['Date'] + ' ' + df_cgm['Time'])


df_cgm.set_index(pd.DatetimeIndex(df_cgm['tstamp']))



for row in df_cgm[::-1].iterrows():
  if(timestamp < row[1]['tstamp']):
    timestamp = pd.to_datetime(row[1]['Date'] + ' ' + row[1]['Time'])
    break

index = int(df_cgm.index[df_cgm['tstamp'] == timestamp][0])

auto_df = df_cgm[:index+1]
manual_df = df_cgm[index+1:]

manual_df = manual_df.set_index(pd.DatetimeIndex(pd.to_datetime(manual_df['Time']).values))
auto_df = auto_df.set_index(pd.DatetimeIndex(pd.to_datetime(auto_df['Time']).values))


result = {}
result['Manual Mode'] ={}
result['Auto Mode'] = {}


##Manual Parameters


##Whole Day

days = manual_df.groupby(['Date']).count().shape[0]

df_final = pd.DataFrame()

df_final['hyperglycemia'] = manual_df[manual_df['Sensor Glucose (mg/dL)'] > 180].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hyperglycemia_critical'] = manual_df[manual_df['Sensor Glucose (mg/dL)'] > 250].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range'] = manual_df[(manual_df['Sensor Glucose (mg/dL)'] >= 70) & (manual_df['Sensor Glucose (mg/dL)'] <= 180)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range_secondary'] = manual_df[(manual_df['Sensor Glucose (mg/dL)'] >= 70) & (manual_df['Sensor Glucose (mg/dL)'] <= 150)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia'] = manual_df[manual_df['Sensor Glucose (mg/dL)'] < 70].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia_level2'] = manual_df[manual_df['Sensor Glucose (mg/dL)'] < 54].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288

result['Manual Mode']['aa'] = df_final['hyperglycemia'].sum()/days
result['Manual Mode']['ab'] = df_final['hyperglycemia_critical'].sum()/days
result['Manual Mode']['ac'] = df_final['range'].sum()/days
result['Manual Mode']['ad'] = df_final['range_secondary'].sum()/days
result['Manual Mode']['ae'] = df_final['hypoglycemia'].sum()/days
result['Manual Mode']['af'] = df_final['hypoglycemia_level2'].sum()/days

##Daytime

manual_df_day = manual_df.between_time('06:00:00', '23:59:59')

df_final['hyperglycemia'] = manual_df_day[manual_df_day['Sensor Glucose (mg/dL)'] > 180].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hyperglycemia_critical'] = manual_df_day[manual_df_day['Sensor Glucose (mg/dL)'] > 250].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range'] = manual_df_day[(manual_df_day['Sensor Glucose (mg/dL)'] >= 70) & (manual_df_day['Sensor Glucose (mg/dL)'] <= 180)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range_secondary'] = manual_df_day[(manual_df_day['Sensor Glucose (mg/dL)'] >= 70) & (manual_df_day['Sensor Glucose (mg/dL)'] <= 150)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia'] = manual_df_day[manual_df_day['Sensor Glucose (mg/dL)'] < 70].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia_level2'] = manual_df_day[manual_df_day['Sensor Glucose (mg/dL)'] < 54].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288

result['Manual Mode']['ba'] = df_final['hyperglycemia'].sum()/days
result['Manual Mode']['bb'] = df_final['hyperglycemia_critical'].sum()/days
result['Manual Mode']['bc'] = df_final['range'].sum()/days
result['Manual Mode']['bd'] = df_final['range_secondary'].sum()/days
result['Manual Mode']['be'] = df_final['hypoglycemia'].sum()/days
result['Manual Mode']['bf'] = df_final['hypoglycemia_level2'].sum()/days

##Night

manual_df_night = manual_df.between_time('00:00:00', '05:59:59')

df_final['hyperglycemia'] = manual_df_night[manual_df_night['Sensor Glucose (mg/dL)'] > 180].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hyperglycemia_critical'] = manual_df_night[manual_df_night['Sensor Glucose (mg/dL)'] > 250].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range'] = manual_df_night[(manual_df_night['Sensor Glucose (mg/dL)'] >= 70) & (manual_df_night['Sensor Glucose (mg/dL)'] <= 180)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range_secondary'] = manual_df_night[(manual_df_night['Sensor Glucose (mg/dL)'] >= 70) & (manual_df_night['Sensor Glucose (mg/dL)'] <= 150)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia'] = manual_df_night[manual_df_night['Sensor Glucose (mg/dL)'] < 70].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia_level2'] = manual_df_night[manual_df_night['Sensor Glucose (mg/dL)'] < 54].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288

result['Manual Mode']['ca'] = df_final['hyperglycemia'].sum()/days
result['Manual Mode']['cb'] = df_final['hyperglycemia_critical'].sum()/days
result['Manual Mode']['cc'] = df_final['range'].sum()/days
result['Manual Mode']['cd'] = df_final['range_secondary'].sum()/days
result['Manual Mode']['ce'] = df_final['hypoglycemia'].sum()/days
result['Manual Mode']['cf'] = df_final['hypoglycemia_level2'].sum()/days

print(result)


##Whole Day

days = auto_df.groupby(['Date']).count().shape[0]

df_final = pd.DataFrame()

df_final['hyperglycemia'] = auto_df[auto_df['Sensor Glucose (mg/dL)'] > 180].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hyperglycemia_critical'] = auto_df[auto_df['Sensor Glucose (mg/dL)'] > 250].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range'] = auto_df[(auto_df['Sensor Glucose (mg/dL)'] >= 70) & (auto_df['Sensor Glucose (mg/dL)'] <= 180)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range_secondary'] = auto_df[(auto_df['Sensor Glucose (mg/dL)'] >= 70) & (auto_df['Sensor Glucose (mg/dL)'] <= 150)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia'] = auto_df[auto_df['Sensor Glucose (mg/dL)'] < 70].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia_level2'] = auto_df[auto_df['Sensor Glucose (mg/dL)'] < 54].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288

result['Auto Mode']['aa'] = df_final['hyperglycemia'].sum()/days
result['Auto Mode']['ab'] = df_final['hyperglycemia_critical'].sum()/days
result['Auto Mode']['ac'] = df_final['range'].sum()/days
result['Auto Mode']['ad'] = df_final['range_secondary'].sum()/days
result['Auto Mode']['ae'] = df_final['hypoglycemia'].sum()/days
result['Auto Mode']['af'] = df_final['hypoglycemia_level2'].sum()/days

##Daytime

auto_df_day = auto_df.between_time('06:00:00', '23:59:59')

df_final['hyperglycemia'] = auto_df_day[auto_df_day['Sensor Glucose (mg/dL)'] > 180].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hyperglycemia_critical'] = auto_df_day[auto_df_day['Sensor Glucose (mg/dL)'] > 250].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range'] = auto_df_day[(auto_df_day['Sensor Glucose (mg/dL)'] >= 70) & (auto_df_day['Sensor Glucose (mg/dL)'] <= 180)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range_secondary'] = auto_df_day[(auto_df_day['Sensor Glucose (mg/dL)'] >= 70) & (auto_df_day['Sensor Glucose (mg/dL)'] <= 150)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia'] = auto_df_day[auto_df_day['Sensor Glucose (mg/dL)'] < 70].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia_level2'] = auto_df_day[auto_df_day['Sensor Glucose (mg/dL)'] < 54].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288

result['Auto Mode']['ba'] = df_final['hyperglycemia'].sum()/days
result['Auto Mode']['bb'] = df_final['hyperglycemia_critical'].sum()/days
result['Auto Mode']['bc'] = df_final['range'].sum()/days
result['Auto Mode']['bd'] = df_final['range_secondary'].sum()/days
result['Auto Mode']['be'] = df_final['hypoglycemia'].sum()/days
result['Auto Mode']['bf'] = df_final['hypoglycemia_level2'].sum()/days

##Night

auto_df_night = auto_df.between_time('00:00:00', '05:59:59')

df_final['hyperglycemia'] = auto_df_night[auto_df_night['Sensor Glucose (mg/dL)'] > 180].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hyperglycemia_critical'] = auto_df_night[auto_df_night['Sensor Glucose (mg/dL)'] > 250].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range'] = auto_df_night[(auto_df_night['Sensor Glucose (mg/dL)'] >= 70) & (auto_df_night['Sensor Glucose (mg/dL)'] <= 180)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['range_secondary'] = auto_df_night[(auto_df_night['Sensor Glucose (mg/dL)'] >= 70) & (auto_df_night['Sensor Glucose (mg/dL)'] <= 150)].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia'] = auto_df_night[auto_df_night['Sensor Glucose (mg/dL)'] < 70].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288
df_final['hypoglycemia_level2'] = auto_df_night[auto_df_night['Sensor Glucose (mg/dL)'] < 54].groupby(['Date'])['Sensor Glucose (mg/dL)'].count()*100/288

result['Auto Mode']['ca'] = df_final['hyperglycemia'].sum()/days
result['Auto Mode']['cb'] = df_final['hyperglycemia_critical'].sum()/days
result['Auto Mode']['cc'] = df_final['range'].sum()/days
result['Auto Mode']['cd'] = df_final['range_secondary'].sum()/days
result['Auto Mode']['ce'] = df_final['hypoglycemia'].sum()/days
result['Auto Mode']['cf'] = df_final['hypoglycemia_level2'].sum()/days


result['Manual Mode']['dd'] = 1.1
result['Auto Mode']['dd'] = 1.1

# print(result)
final = pd.DataFrame.from_dict(result, orient='index', columns=['ca','cb','cc','cd','ce','cf','ba','bb','bc','bd','be','bf','aa','ab','ac','ad','ae','af','dd'])
final[::-1].to_csv('Results.csv', header=False, index=False,index_label=['Manual Mode','Auto Mode'])

