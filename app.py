import streamlit as st
import pandas as pd

# Tytuł aplikacji
st.title("Analiza danych z oswidczen majatkowych poslow na sejm")
st.write("Do analizy wzieto dane z oswiadczen majatkowych poslow dotyczacych tylko domow i miekszan (inne nieruchomosci zostaly pominiete).") 
st.write("Jesli wystepuja zrozbieznosci miedzy wartosciami rzeczywisymi z oswiadczenia to prosze dac znac, poprawie.")
# Wczytanie danych
try:
    df = pd.read_csv("parlament.csv")
    
    # Sprawdzenie kolumny 'lista'
    if 'lista' not in df.columns:
        st.error("Plik nie zawiera kolumny 'lista'.")
    else:
        # Filtrowanie po 'lista'
        unique_lista = df['lista'].unique()
        selected_lista = st.multiselect(
            "Wybierz wartości z kolumny 'lista':",
            options=unique_lista,
            default=unique_lista
        )
        filtered_df = df[df['lista'].isin(selected_lista)]
        
        # Wyświetlenie tabeli
        st.write("Przefiltrowana tabela:")
        st.dataframe(filtered_df)
        
        # Kolumny do obliczenia średniej
        numeric_columns = [
            'suma wartosci wszystkich domow lub mieszkan',
            'suma powierzchni',
            'cena za metr'
        ]
        
        # Konwersja kolumn na liczby (ignorowanie błędów)
        for col in numeric_columns:
            filtered_df[col] = pd.to_numeric(filtered_df[col], errors='coerce')
        
        # Obliczenie średnich
        mean_values = filtered_df[numeric_columns].mean(skipna=True)
        
        # Wyświetlenie średnich
        st.write("### Średnie wartości:")
        for col, mean_val in mean_values.items():
            st.write(f"**{col}**: {mean_val:.2f}")
        
except FileNotFoundError:
    st.error("Nie znaleziono pliku 'parlament.csv'. Upewnij się, że plik znajduje się w tym samym folderze co aplikacja.")
