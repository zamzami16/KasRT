"""
Requirements:
   pip install streamlit
   pip install streamlit-aggrid
"""

from datetime import datetime
import pytz
import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid

pesan = """
Assalamu'alaikum Wr. Wb.
Niki wonten error teng aplikasi KasRT, mohon pencerahannya.
"""
st.set_page_config(
    page_title="KAS RT",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": f"https://api.whatsapp.com/send/?phone=6285161400863text={pesan}&type=phone_number&app_absent=0",
        "About": "# Created by mohyusufz.",
    },
)


st.write("# **KAS KAS RT.**")

# excel_data = "https://docs.google.com/spreadsheets/d/1hdNOhGoTdkIVqioERIcdLlN3NgayhJtUEf-BDYScYsk/edit?usp=share_link";

url = "https://docs.google.com/spreadsheets/d/1VEH6yTzrgEgaoG7a2giZG4C4I4ACM1ZxHZoXBsewZ0M/edit#gid=1357825882"
url_1 = url.replace("/edit#gid=", "/export?format=csv&gid=")

df = pd.read_csv(url_1)

saldo = []
for i in range(len(df)):
    masuk = df.iloc[0 : i + 1]["Pemasukan"].sum()
    keluar = df.iloc[0 : i + 1]["Pengeluaran"].sum()
    saldo.append(masuk - keluar)

df["Saldo"] = saldo
df["Editor"] = df["Email Address"]
# print(df.columns.tolist())
dff = df[
    ["Timestamp", "Pemasukan", "Pengeluaran", "Saldo", "Keterangan", "Editor"]
]

# AgGrid
gb = GridOptionsBuilder.from_dataframe(dff)
gb.configure_auto_height()
gb.configure_column(
    "Timestamp",
    type=["customDateTimeFormat", "nonEditableColumn"],
    custom_format_string="yyyy-mm-dd",
)
gb.configure_column(
    "Pemasukan",
    type=["numericColumn", "customCurrencyFormat"],
    custom_currency_symbol="Rp",
)
gb.configure_column(
    "Pengeluaran",
    type=["numericColumn", "customCurrencyFormat"],
    custom_currency_symbol="Rp",
)
gb.configure_column(
    "Saldo",
    type=["numericColumn", "customCurrencyFormat"],
    custom_currency_symbol="Rp",
)

gridOptions = gb.build()

# st.write("### Streamlit AgGrid")
AgGrid(dff, gridOptions=gridOptions)

st.write(
    "### Saldo sekarang Tgl: {1} | Rp{0}".format(
        dff["Pemasukan"].sum() - dff["Pengeluaran"].sum(),
        datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%d-%m-%Y"),
    )
)

# st.write("Created with :purple_heart: by Zami16")
st.markdown(
    """<div style="text-align: center"> Created with &#128153; by Zami16 </div>""",
    unsafe_allow_html=True,
)
