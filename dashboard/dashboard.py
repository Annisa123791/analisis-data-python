import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul Dashboard
st.title("Proyek Analisis Data: Bike Sharing Dataset :sparkles:")
# st.markdown("- **Nama:** Annisa Saninah")
# st.markdown("- **Email:** saninahannisa@gmail.com") 
# st.markdown("- **ID Dicoding:** annisa1212") 

# Membaca data
all_df = pd.read_csv("https://raw.githubusercontent.com/Annisa123791/analisis-data-python/refs/heads/main/dashboard/all_df.csv")
all_df["dteday"] = pd.to_datetime(all_df["dteday"], errors='coerce')
all_df = all_df.dropna(subset=["dteday"])

# Mengelompokkan data berdasarkan jam dan menghitung jumlah peminjaman sepeda
hourly_rentals = all_df.groupby("hr")["cnt_hour"].sum()

# Mengelompokkan data berdasarkan kondisi cuaca dan menghitung jumlah peminjaman sepeda
weather_rentals = all_df.groupby("weathersit_day")["cnt_day"].sum().sort_values(ascending=False)

with st.sidebar:
    st.title("Proyek Nisa")
    st.image("logo.png")
    st.title("Filter")

# Pastikan kolom tanggal tidak ada nilai NaN
all_df = all_df.dropna(subset=["dteday"])

min_date = all_df["dteday"].min().date()
max_date = all_df["dteday"].max().date()

start_date = st.date_input("Tanggal Mulai", min_date)
end_date = st.date_input("Tanggal Akhir", max_date)

# Convert 'dteday' to datetime if it isn't already
all_df['dteday'] = pd.to_datetime(all_df['dteday'], errors='coerce')

# Filter data based on the selected date range
filtered_df = all_df[
    (all_df['dteday'] >= pd.Timestamp(start_date)) & 
    (all_df['dteday'] <= pd.Timestamp(end_date))
]

# Pertanyaan 1: Bagaimana pola peminjaman sepeda berdasarkan jam dalam sehari?
hourly_rentals = filtered_df.groupby("hr")["cnt_hour"].sum()
st.header("Jumlah peminjaman sepeda berdasarkan jam")
st.dataframe(hourly_rentals)

# Visualisasi 1: Peminjaman Sepeda Berdasarkan Jam
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hourly_rentals.index, y=hourly_rentals.values, marker="o", ax=ax)
ax.set_title("Pola Peminjaman Sepeda Berdasarkan Jam dalam Sehari")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Pertanyaan 2: Bagaimana pengaruh kondisi cuaca terhadap jumlah peminjaman sepeda?
filtered_df.groupby("weathersit_day")["cnt_day"].sum().sort_values(ascending=False)
st.header("Jumlah peminjaman sepeda berdasarkan kondisi cuaca")
st.dataframe(weather_rentals)

# Visualisasi 2: Pengaruh Cuaca terhadap Peminjaman
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=weather_rentals.index, y=weather_rentals.values, palette="coolwarm", ax=ax)
ax.set_title("Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman Sepeda")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig)

# Pertanyaan 3: Bagaimana distribusi jumlah peminjaman sepeda harian?
st.header("Statistik deskriptif jumlah peminjaman sepeda harian")
st.dataframe(filtered_df["cnt_day"].describe())

# Visualisasi 3: Distribusi Jumlah Peminjaman Sepeda Harian
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_df["cnt_day"], bins=30, kde=True, color="blue", ax=ax)
ax.set_title("Distribusi Jumlah Peminjaman Sepeda Harian")
ax.set_xlabel("Jumlah Peminjaman Sepeda")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# Pertanyaan 4: Bagaimana pengaruh suhu terhadap jumlah peminjaman sepeda?
correlation = filtered_df[["temp_day", "cnt_day"]].corr().iloc[0, 1]
st.header(f"Korelasi antara suhu dan jumlah peminjaman sepeda: {correlation:.2f}")

# Visualisasi 4: Hubungan antara Suhu dan Peminjaman Sepeda
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=filtered_df["temp_day"], y=filtered_df["cnt_day"], alpha=0.5, ax=ax)
ax.set_title("Pengaruh Suhu terhadap Jumlah Peminjaman Sepeda")
ax.set_xlabel("Suhu")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig)


