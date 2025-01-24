import pandas as pd
import streamlit as st
import plotly.express as px


def load_df(path: str, name: str):
    df = pd.read_csv(path)
    df = df.drop(columns=['Informazioni cronologiche'])
    col_reddito = 'Reddito annuo lordo (include retribuzione totale + bonus etc o fatturato)'
    df[col_reddito] = df[col_reddito].replace(
        {"meno di 10K": "da 0 a 10K",
         "oltre i 100K": "superiore 100K"},
    )

    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].fillna(-1)
        else:
            df[col] = df[col].fillna('Non specificato')

    # crypto_col = "Percentuale crypto nel Patrimonio? (i valori sono da moltiplicare per 10 - 1 corrisponde al 10%)"
    # stock_col = "Percentuale azionario nel Patrimonio? (i valori sono da moltiplicare per 10 - 1 corrisponde al 10%)"
    # real_estate_col = "Percentuale immobiliare (esclusa prima casa) nel Patrimonio? (i valori sono da moltiplicare per 10 - 1 corrisponde al 10%)"
    # bond_col = "Percentuale obbligazionario (vedi pagina informazioni)"
    # df[bond_col] = 10 - df[stock_col] - df[crypto_col] - df[real_estate_col]
    # df[bond_col] = df[bond_col][(df[bond_col] <= 10) & (df[bond_col] >= 0)]

    st.session_state[name] = df


def create_pie_charts(base_df: pd.DataFrame):
    columns = base_df.columns.tolist()
    for col in columns:
        try:
            st.write(f"Colonna: {col}")

            tmp_df = base_df[col].value_counts().to_frame().join(base_df[col].value_counts(normalize=True))

            total = tmp_df['count'].sum()
            tmp_df = tmp_df.drop(labels=[-1, 'Non specificato'], errors='ignore', axis=0)
            tmp_df = tmp_df.rename(columns={'count': 'Conteggio', 'proportion': 'Percentuale'})
            tmp_df['Risposta'] = tmp_df.index
            tmp_df = tmp_df[['Risposta', 'Conteggio', 'Percentuale']]

            tmp_df = tmp_df.sort_values(by='Risposta', ascending=False)
            tmp_df['Percentuale'] = tmp_df['Percentuale'] * 100
            tmp_df['Percentuale'] = tmp_df['Percentuale'].round(1)

            st.dataframe(tmp_df, use_container_width=True, hide_index=True,
                         column_config={
                             'Percentuale': {'alignment': 'center'},
                             'Conteggio': {'alignment': 'center'},
                         })

            tot_effective = tmp_df["Conteggio"].sum()
            st.write(f'Totale voti effettivi: {tot_effective} (Astenuti: {total - tot_effective})')

            fig = px.pie(tmp_df, values='Conteggio', names='Risposta')
            st.plotly_chart(fig, use_container_width=True, key=f"{col}_pie")
        except Exception as e:
            print(col, base_df[col])
            print(e)


def create_bar_charts(base_df: pd.DataFrame):
    columns = base_df.columns.tolist()
    for col in columns:
        try:
            st.write(col)
            tmp_df = base_df[col].value_counts().to_frame()
            total = tmp_df['count'].sum()
            tmp_df = tmp_df.drop(labels=[-1, 'Non specificato'], errors='ignore', axis=0)
            tmp_df = tmp_df.rename(columns={'count': 'Conteggio'})
            tmp_df['Risposta'] = tmp_df.index
            tmp_df = tmp_df[['Risposta', 'Conteggio']]
            tmp_df = tmp_df.sort_values(by='Conteggio', ascending=False)

            st.dataframe(tmp_df, use_container_width=True, hide_index=True,
                         column_config={
                             'Percentuale': {'alignment': 'center'},
                             'Conteggio': {'alignment': 'center'},
                         })

            tot_effective = tmp_df["Conteggio"].sum()
            st.write(f'Totale voti effettivi: {tot_effective} (Astenuti: {total - tot_effective})')

            toggle = st.toggle(label='Ordina per Risposta o Conteggio', key=f'toggle_{col}')
            tmp_df = tmp_df.sort_values(by='Conteggio' if toggle else 'Risposta', ascending=False)

            fig = px.bar(tmp_df, y='Risposta', x='Conteggio', orientation='h')
            st.plotly_chart(fig, use_container_width=True, key=f"{col}_bar")
            st.divider()
        except Exception as e:
            print(col, base_df[col])
            print(e)
