import functools

from common import load_df, create_pie_charts, create_bar_charts
import streamlit as st


def pie_charts_page(df_name: str):
    st.title('Grafici a torta')
    st.write("NB: anche i grafici sono interattivi, potete oscurare valori cliccando sulla legenda. Questo filtraggio "
             "varrà solo per il grafico con cui interagite, non sull'intero censimento.")
    st.divider()
    df = st.session_state[df_name]
    create_pie_charts(df)


def bar_charts_page(df_name: str):
    st.title('Grafici a barre')
    df = st.session_state[df_name]
    create_bar_charts(df)


load_df('expat_data.csv', 'expat_df')
load_df('it_data.csv', 'it_df')


def intro_page():
    st.title('Censimento ItaliaPersonalFinance')
    st.divider()

    st.markdown("""
    Benvenuti nell'applicativo di consultazione dei risultati del censimento di Italia Personal Finance!
    
    Tramite questo sito potrete consultare i risultati dell'ultimo censimento che si è svolto (attualmente [quello del 2025](https://www.reddit.com/r/ItaliaPersonalFinance/comments/1i3l0y6/censimento_ipf_2025_chi_siete_cosa_portate_un/)) 
    
    Tramite la barra laterale potete accedere ad alcuni grafici base fatti sui dati del censimento e divisi per italiani residenti ed espatriati.
    Sempre tramite la barra potrete filtrare i dati: per ogni domanda presente nel censimento avrete la possibilità di filtrare quali risposte includere nell'analisi, ovviamente di default saranno tutte selezionate.
    """)


pages = st.navigation({
    "Intro": [st.Page(intro_page, title='Informazioni', url_path='intro')],
    "Italiani": [
        st.Page(functools.partial(pie_charts_page, df_name='it_df'), title='Grafici a torta', url_path='ita_pie_charts'),
        st.Page(functools.partial(bar_charts_page, df_name='it_df'), title='Grafici a barre', url_path='ita_bar_charts')
    ],
    'Expat': [
        st.Page(functools.partial(pie_charts_page, df_name='expat_df'), title='Grafici a torta', url_path='exp_pie_charts'),
        st.Page(functools.partial(bar_charts_page, df_name='expat_df'), title='Grafici a barre', url_path='exp_bar_charts')
    ]
})

it_expander = st.sidebar.expander("Filtri ITA")
for col in st.session_state['it_df'].columns.tolist():
    col_select = it_expander.multiselect(label=col, options=st.session_state['it_df'][col].unique(),
                                         default=st.session_state['it_df'][col].dropna().unique(),
                                         key=f'it_{col}')
    st.session_state['it_df'] = st.session_state['it_df'][st.session_state['it_df'][col].isin(col_select)]

expat_expander = st.sidebar.expander("Filtri Expat")

for col in st.session_state['expat_df'].columns.tolist():
    col_select = expat_expander.multiselect(label=col, options=st.session_state['expat_df'][col].unique(),
                                            default=st.session_state['expat_df'][col].dropna().unique(),
                                            key=f"expat_{col}")
    st.session_state['expat_df'] = st.session_state['expat_df'][st.session_state['expat_df'][col].isin(col_select)]

theme_btn = st.sidebar.toggle('Cambia tema', key='toggle_theme')
if theme_btn:
    st._config.set_option('theme.base', 'light')
else:
    st._config.set_option('theme.base', 'dark')

pages.run()
