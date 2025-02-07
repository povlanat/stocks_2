import streamlit as st
import pandas as pd
import datetime


st.set_page_config(layout="wide")

@st.cache_data
def load_data_1():
    return pd.read_csv('df_final_filter_1.csv').reset_index(drop=True)

@st.cache_data
def load_data_final():
    return pd.read_csv('df_final.csv', parse_dates=[0]).reset_index(drop=True)

df= load_data_final()
df_1 = load_data_1()
    


st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)
with col1:
    with st.expander("Фильтры первого уровня"):

        # Создание формы
        with st.form(key="filters_form_1"):

            # Капитализация (две колонки)
            cap1, cap2 = st.columns([1, 1])
            with cap1:
                market_cap_min = st.number_input("Капитализация (млн $) От", value=None)
            with cap2:
                market_cap_max = st.number_input("Капитализация (млн $) До", value=None)

            # Бета компании (две колонки)
            std1, std2 = st.columns([1, 1])
            with std1:
                beta_min = st.number_input("Бета От", value=None)
            with std2:
                beta_max = st.number_input("Бета До", value=None)

            # Даты (две колонки)
            t1, t2 = st.columns([1, 1])
            with t1:
                date_1 = st.date_input("Дата От", value=None, min_value=datetime.date(2004, 1, 1))
            with t2:
                date_2 = st.date_input("Дата До", value=None, min_value=datetime.date(2004, 1, 1))

            # Страна и объем торгов (две колонки)
            c1, c2 = st.columns([1, 1])
            with c1:
                country = st.selectbox("Страна акции", ("кроме Китая", "Китай"))
            with c2:
                volume = st.number_input("Объем торгов (тыс. $) От", value=None)

            cols = st.columns(2)
            with cols[0]:
                index = st.multiselect('Index', options=['SP500', 'Russel', 'Nasdaq'],
                                       default = ['SP500', 'Russel', 'Nasdaq'])
            with cols[1]:
                sectors = ['Financial Services', 'Industrials', 'Technology', 'Energy',
                            'Consumer Cyclical', 'Utilities', 'Healthcare',
                            'Consumer Defensive', 'Basic Materials', 'Real Estate',
                            'Communication Services']
                sector = st.multiselect('Сектор', options=sectors,
                                       default = sectors)


            # Кнопка "Применить"
            apply_button = st.form_submit_button(label="Применить")


with col2:
    with st.expander("Фильтры второго уровня"):

        # Создание формы
        with st.form(key="filters_form_2"):
            # RSI
            cols = st.columns(2)
            with cols[0]:
                rsi_min = st.number_input("RSI от ", value=None)
            with cols[1]:
                rsi_max = st.number_input("RSI до", value=None)
            
            # dX - d index за пред отчетный период
            cols = st.columns(2)
            with cols[0]:
                f_2_2_min = st.number_input("dX - d index за пред отчетный период  (%) От", value=None)
            with cols[1]:
                f_2_2_max = st.number_input("dX - d index за пред отчетный период  (%) До", value=None)

            # dX - d ETF за пред отчетный период
            cols = st.columns(2)
            with cols[0]:
                f_2_3_min = st.number_input("dX - d ETF за пред отчетный период  (%) От", value=None)
            with cols[1]:
                f_2_3_max = st.number_input("dX - d ETF за пред отчетный период  (%) До", value=None)

            # Кнопка "Применить"
            apply_button = st.form_submit_button(label="Применить")

with col3:
    with st.expander("Фильтры третьего уровня"):
        # Создание формы
        with st.form(key="filters_form_3"):
            cols = st.columns(2)
            with cols[0]:
                f_3_1_min = st.number_input("Отношение изменения (мультипликатор) От", value=None)
            with cols[1]:
                f_3_1_max = st.number_input("Отношение изменения (мультипликатор) До", value=None)

            cols = st.columns(2)
            options = ['Без фильтра'] + [f'рост_{i}' for i in range(1, 6)] + [f'падение_{i}' for i in range(1, 6)]
            with cols[0]:
                f_3_2 = st.selectbox("Форма свечи", options=options)
            with cols[1]:
                if f_3_2!='Без фильтра':
                    st.image(f'fig/{f_3_2}.png')

            cols = st.columns(2)
            with cols[0]:
                f_3_3_min = st.number_input("Отношение объема (мультипликатор) От", value=None)
            with cols[1]:
                f_3_3_max = st.number_input("Отношение объема (мультипликатор) До", value=None)

            # Кнопка "Применить"
            apply_button = st.form_submit_button(label="Применить")


# Инициализация начальных условий фильтрации (True для всех строк)
filter_condition_df = pd.Series([True] * len(df))
filter_condition_df_1 = pd.Series([True] * len(df_1))

# Применение фильтров первого уровня
if date_1 is not None:
    date_1_dt = pd.to_datetime(date_1)
    filter_condition_df &= df['Date'] >= date_1_dt
    filter_condition_df_1 &= df_1['Year'] >= date_1_dt.year

if date_2 is not None:
    date_2_dt = pd.to_datetime(date_2)
    filter_condition_df &= df['Date'] <= date_2_dt
    filter_condition_df_1 &= df_1['Year'] <= date_2_dt.year

# Фильтрация по символам после группировки
df_group = df_1[filter_condition_df_1].groupby(['symbol', 'index', 'sector'], as_index=False).mean()

if market_cap_min is not None:
    df_group = df_group[df_group['marketCap'] >= market_cap_min]
if market_cap_max is not None:
    df_group = df_group[df_group['marketCap'] <= market_cap_max]

if beta_min is not None:
    df_group = df_group[df_group['beta'] >= beta_min]
if beta_max is not None:
    df_group = df_group[df_group['beta'] <= beta_max]


if country == "кроме Китая":
    df_group = df_group[df_group['country_not_CN'] == 1]
else:
    df_group = df_group[df_group['country_not_CN'] == 0]

if volume is not None:
    df_group = df_group[df_group['Volume'] >= volume * 1000]

if index is not None:
    df_group = df_group[df_group['index'].isin(index)]

if sector is not None:
    df_group = df_group[df_group['sector'].isin(sector)]

# Обновление условия фильтрации для df
filter_condition_df &= df['symbol'].isin(list(df_group['symbol']))

# Применение фильтров второго уровня для df
if rsi_min is not None:
    filter_condition_df &= df['RSI'] >= rsi_min
if rsi_max is not None:
    filter_condition_df &= df['RSI'] <= rsi_max

if f_2_2_min is not None:
    filter_condition_df &= df['filter_2_2'] >= f_2_2_min
if f_2_2_max is not None:
    filter_condition_df &= df['filter_2_2'] <= f_2_2_max

if f_2_3_min is not None:
    filter_condition_df &= df['filter_2_3'] >= f_2_3_min
if f_2_3_max is not None:
    filter_condition_df &= df['filter_2_3'] <= f_2_3_max

# Применение фильтров третьего уровня для df
if f_3_1_min is not None:
    filter_condition_df &= df['filter_3_1'] >= f_3_1_min
if f_3_1_max is not None:
    filter_condition_df &= df['filter_3_1'] <= f_3_1_max

if (f_3_2 is not None) and (f_3_2 != 'Без фильтра'):
    filter_condition_df &= df['filter_3_2'] == f_3_2

if f_3_3_min is not None:
    filter_condition_df &= df['filter_3_3'] >= f_3_3_min
if f_3_3_max is not None:
    filter_condition_df &= df['filter_3_3'] <= f_3_3_max

# Применение фильтрации к df и df_1
df_filtered = df[filter_condition_df]

all = st.checkbox('До следующего отчета')
if not all:
    n = st.select_slider('количество торговых дней', options = range(1,51))
else:
    n = 'all'
# Отображение графика
st.bar_chart(df_filtered[f'target_{n}'].value_counts().reindex(range(-60, 61), fill_value=0), height=400)

# Расчет среднего значения и стандартного отклонения
count_target = df_filtered[f"target_{n}"].count()
mean_target = df_filtered[f"target_{n}"].mean()
std_target = df_filtered[f"target_{n}"].std()

# Вывод количества отфильтрованных строк
st.write(f"Количество отфильтрованных данных: {count_target}")

# Вывод среднего значения и стандартного отклонения
st.write(f"Среднее значение Target: {mean_target:.2f} %")
st.write(f"Стандартное отклонение Target: {std_target:.2f} %")