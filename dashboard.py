import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_casual_df(df):
    casual_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "casual": "sum"
    })
    casual_df = casual_df.reset_index()
    casual_df.rename(columns={
        "instant": "ride_id",
        "casual": "casual_rider"
    }, inplace=True)
    
    return casual_df

def create_registered_df(df):
    registered_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "registered": "sum"
    })
    registered_df = registered_df.reset_index()
    registered_df.rename(columns={
        "instant": "ride_id",
        "registered": "registered_rider"
    }, inplace=True)
    
    return registered_df

df_day=pd.read_csv('https://raw.githubusercontent.com/ailzaza/dashboard_streamlit/main/day.csv')
# df_hour=pd.read_csv('/content/drive/MyDrive/Dataset_Dicoding/hour.csv')
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filter_main = df_day[(df_day['dteday'] >= str(start_date)) & (df_day['dteday'] <= str(end_date))]

casual_df = create_casual_df(filter_main)
registered_df = create_registered_df(filter_main)
# cnt_df = create_cnt_df(filter_main)

st.header('Dashboard: bike sharing')
st.subheader('total riders')

col1, col2 = st.columns(2)

with col1:
    total_casual_riders = casual_df.casual_rider.sum()
    st.metric("Total casual riders", value=total_casual_riders)

with col2:
    total_registered_riders = registered_df.registered_rider.sum()
    st.metric("Total registered riders", value=total_registered_riders)

# usetotal_day = df_day['cnt']
# usetotal_day

st.subheader('pertanyaan 1')

print('Banyak null dalam satu kolom:')
df_day.isnull().sum()

print('Banyak duplicate dalam satu kolom:')
df_day.duplicated().sum()

df_day.dropna(axis=0, inplace=True)


print(df_day['dteday'])

result = df_day[df_day['dteday'] == '2011-01-08']['cnt']

result_str = result.to_string(index=False, header=False)
st.metric(label='hari pertama pada minggu kedua', value=result)

week_sum= df_day['registered'].iloc[0:7].sum()
print(week_sum)

week_sumc= df_day['casual'].iloc[0:7].sum()
print(week_sumc)

start_date1 = pd.to_datetime('2011-01-01')
end_date1 = pd.to_datetime('2011-01-10')
filter_date1 = df_day[(df_day['dteday'] >= start_date1) & (df_day['dteday'] <= end_date1)]
fig, ax = plt.subplots(figsize=(16, 8))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"]
sns.barplot(
        y='cnt',
        x='dteday',
        data= filter_date1,
        palette=colors,
        ax=ax
    )
ax.set_xticks(ticks=filter_date1.index,labels=filter_date1['dteday'].dt.strftime('%d %b'))
ax.set_ylabel('total')
ax.set_xlabel('tanggal')
st.pyplot(fig)

st.subheader('pertanyaan 2')

start_date2 = pd.to_datetime('2011-01-01')
end_date2 = pd.to_datetime('2011-01-07')
filter_date2 = df_day[(df_day['dteday'] >= start_date2) & (df_day['dteday'] <= end_date2)]
# Menghitung total casual dan registered
total_casual = filter_date2['casual'].sum()
total_registered = filter_date2['registered'].sum()
col1, col2 = st.columns(2)
with col1:
    st.metric(label='total registered', value=total_registered)
with col2:
    st.metric(label='total casual', value=total_casual)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9"]

sns.barplot(y="dteday", x="registered", data=filter_date2, palette=colors, ax=ax[0])
ax[0].set_xlabel('registered', fontsize=30)
ax[0].set_title("registered day 1-7", loc="center", fontsize=50)
ax[0].set_ylabel('tanggal', fontsize=30)
ax[0].set_yticks(ticks=filter_date2.index)
ax[0].set_yticklabels(filter_date2['dteday'].dt.strftime('%d %b'))
ax[0].tick_params(axis='both', labelsize=30)

sns.barplot(y="dteday", x="casual", data=filter_date2, palette=colors, ax=ax[1])
ax[1].set_xlabel('casual', fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("casual day 1-7", loc="center", fontsize=50)
ax[1].set_ylabel('tanggal', fontsize=30)
ax[1].set_yticks(ticks=filter_date2.index)
ax[1].set_yticklabels(filter_date2['dteday'].dt.strftime('%d %b'))
ax[1].tick_params(axis='both', labelsize=30)

st.pyplot(fig)

"""## Conclusion

- Conclution pertanyaan 1
banyaknya jumlah rental pada hari pertama di minggu kedua adalah 959 riders

- conclution pertanyaan 2
banyaknya jumlah pengguna register pada minggu pertama adalah 8405 riders dan jumlah pengguna casual pada minggu pertama adalah 1008 riders
"""
