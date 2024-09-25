import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/day.csv') 
    return df

df = load_data()

# Dashboard Title
st.title('Dashboard Analisis Penyewaan Sepeda')
st.markdown("""
    Dashboard ini memberikan visualisasi data penyewaan sepeda berdasarkan berbagai faktor seperti kondisi cuaca, musim, dan suhu terasa. 
    Anda dapat menggunakan filter di sidebar untuk menganalisis tren penyewaan sepeda berdasarkan kriteria tertentu.
""")

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("Gambar/pngwing.com (3).png")
    
# Sidebar filters
st.sidebar.header('Filter Data')
weather_labels = {
    1: 'Cerah',
    2: 'Mendung',
    3: 'Hujan Ringan/Snow',
}
season_labels = {
    1: 'Musim Dingin',
    2: 'Musim Semi',
    3: 'Musim Panas',
    4: 'Musim Gugur',
}


    
# Filter based on weather condition
st.sidebar.subheader("Filter Berdasarkan Kondisi Cuaca")
weather_options = df['weathersit'].unique()
selected_weather = st.sidebar.multiselect('Pilih Kondisi Cuaca:', 
                                           [weather_labels[i] for i in weather_options], 
                                           default=[weather_labels[i] for i in weather_options])

# Filter based on season
st.sidebar.subheader("Filter Berdasarkan Musim")
season_options = df['season'].unique()
selected_season = st.sidebar.multiselect('Pilih Musim:', 
                                          [season_labels[i] for i in season_options], 
                                          default=[season_labels[i] for i in season_options])
selected_weather_values = [key for key, value in weather_labels.items() if value in selected_weather]
selected_season_values = [key for key, value in season_labels.items() if value in selected_season]


filtered_df = df[(df['weathersit'].isin(selected_weather_values)) & (df['season'].isin(selected_season_values))]

# Display dataset
st.subheader('Data Penyewaan Sepeda (Terfilter)')
st.write(filtered_df)
st.subheader('Pengaruh Kondisi Cuaca Terhadap Penyewaan Sepeda')
weather_rental_mean = filtered_df.groupby('weathersit')['cnt'].mean()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=[weather_labels[i] for i in weather_rental_mean.index], y=weather_rental_mean.values, palette='coolwarm', ax=ax)


for i, v in enumerate(weather_rental_mean.values):
    ax.text(i, v + 0.5, f"{v:.2f}", ha='center', fontsize=10, color='black')

ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=14)
ax.set_xlabel('Kondisi Cuaca', fontsize=12)
ax.set_ylabel('Rata-rata Jumlah Penyewaan Sepeda', fontsize=12)
ax.tick_params(axis='x', rotation=45) 
st.pyplot(fig)

st.markdown("""
    **Interpretasi**: Rata-rata penyewaan sepeda lebih tinggi pada kondisi cuaca cerah dibandingkan saat hujan atau salju. Ini menunjukkan bahwa cuaca yang lebih baik memiliki korelasi dengan peningkatan penggunaan sepeda.
""")

# Scatter plot between atemp and cnt
st.subheader('Hubungan Suhu Terasa dengan Jumlah Penyewaan Sepeda')
fig, ax = plt.subplots(figsize=(8, 5))
scatter = sns.scatterplot(x=filtered_df['atemp'], y=filtered_df['cnt'], hue=filtered_df['season'], palette='deep', ax=ax)

# Add title and labels
ax.set_title('Hubungan Suhu Terasa dengan Jumlah Penyewaan Sepeda', fontsize=14)
ax.set_xlabel('Suhu Terasa (atemp)', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=12)

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Musim')

ax.grid(True, linestyle='--', alpha=0.7)

st.pyplot(fig)

st.markdown("""
    **Interpretasi**: Plot ini menunjukkan hubungan antara suhu terasa (atemp) dan jumlah penyewaan sepeda. Titik-titik diwarnai berdasarkan musim, memberikan gambaran yang lebih jelas tentang bagaimana musim juga memengaruhi penyewaan.
""")


st.subheader('Kesimpulan')

# Generate conclusions based on trends in the data
def generate_conclusions(df):
    conclusions = []

  
    weather_rental_mean = df.groupby('weathersit')['cnt'].mean()
    if weather_rental_mean.idxmax() == 1:
        conclusions.append("Jumlah penyewaan sepeda tertinggi terjadi saat cuaca cerah.")
    elif weather_rental_mean.idxmax() == 2:
        conclusions.append("Jumlah penyewaan sepeda tertinggi terjadi saat cuaca mendung atau berawan.")
    else:
        conclusions.append("Jumlah penyewaan sepeda tertinggi terjadi saat cuaca hujan ringan atau salju.")

 
    correlation_atemp_cnt = df['atemp'].corr(df['cnt'])
    if correlation_atemp_cnt > 0:
        conclusions.append(f"Suhu terasa (atemp) memiliki korelasi positif dengan penyewaan sepeda. Korelasi: {correlation_atemp_cnt:.2f}.")
    else:
        conclusions.append(f"Suhu terasa (atemp) memiliki korelasi negatif dengan penyewaan sepeda. Korelasi: {correlation_atemp_cnt:.2f}.")

    
    season_rental_mean = df.groupby('season')['cnt'].mean()
    if season_rental_mean.idxmax() == 3:
        conclusions.append("Penyewaan sepeda tertinggi terjadi pada musim panas.")
    elif season_rental_mean.idxmax() == 2:
        conclusions.append("Penyewaan sepeda tertinggi terjadi pada musim semi.")
    else:
        conclusions.append(f"Penyewaan sepeda tertinggi terjadi pada musim {season_labels[season_rental_mean.idxmax()]}.")
    
    return conclusions


conclusions = generate_conclusions(filtered_df)
for conclusion in conclusions:
    st.write(f"- {conclusion}")

st.markdown("""
    **Analisis Lanjutan**: Dengan menggunakan hasil dari dashboard ini, Anda dapat melihat bagaimana cuaca, musim, dan suhu terasa mempengaruhi jumlah penyewaan sepeda. Informasi ini berguna bagi bisnis penyewaan sepeda atau perencanaan transportasi kota.
""")

# Footer
st.sidebar.text('Dashboard by Arjuna')
