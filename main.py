import tkinter
import yfinance as yf
from tkinter import *


# Okno:
window = Tk()
window.title("DCF model")
window.minsize(300, 300)
window.resizable(False, False)
#window.iconbitmap("icon_Dollar.ico")

# Barvy:
window.config(bg="#127369")

# Funkce pro získání aktuální ceny:
def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    price = stock.history(period="1d")["Close"].iloc[0]
    return price

# Funkce pro formátování čísel:
def format_large_number(number):
    return f"{number:,.2f}"

# Funkce pro získání Free Cash Flow:
def get_free_cash_flow(ticker):
    stock = yf.Ticker(ticker)
    cash_flow = stock.cashflow
    if "Free Cash Flow" in cash_flow.index:
        fcf = cash_flow.loc["Free Cash Flow"][0]
        return fcf
    else:
        raise ValueError("Nelze načíst FCF pro tento Ticker.")

# Funkce na výpočet vnitřní hodnoty akcie:
def calculate_dcf(fcf, growth_rate, discount_rate, years, shares_outstanding):
    dcf_value = 0
    for year in range(1, years + 1):
        future_fcf = fcf * ((1 + growth_rate) ** year)
        present_value = future_fcf / ((1 + discount_rate) ** year)
        dcf_value += present_value
        
    # Přepočet na hodnotu akcii:
    dcf_value_per_share = dcf_value / shares_outstanding
    return dcf_value_per_share

# Funkce pro zobrazení výsledků:
def calculate_and_display():
    ticker = ticker_entry.get()
    try:
        # Načtení Free Cash Flow (FCF):
        fcf = get_free_cash_flow(ticker)
        formatted_fcf = format_large_number(fcf)
        fcf_entry.delete(0, tkinter.END)
        fcf_entry.insert(0, formatted_fcf)

        # Načítání růstové míry a diskontní sazby:
        growth_rate = float(growth_entry.get()) / 100
        discount_rate = float(discount_entry.get()) / 100
        years = int(years_entry.get())

        # Získání aktuální ceny:
        current_price = get_current_price(ticker)

        # Počet akcií v oběhu:
        stock = yf.Ticker(ticker)
        shares_outstanding = stock.info.get("sharesOutstanding", 1)

        # Výpočet DCF hodnoty na akcii:
        dcf_value = calculate_dcf(fcf, growth_rate, discount_rate, years, shares_outstanding)

        # Určení podhodnocení nebo nadhodnocení:
        if dcf_value > current_price:
            valuation = "Podhodnocená"
        else:
            valuation = "Nadhodnocená"

        # Zobrazení výsledků:
        result_text.delete(1.0, tkinter.END)
        result_text.insert(tkinter.END, f"Aktuální cena: {current_price:.2f}\n"
                                 f"Vnitřní hodnota (DCF): {dcf_value:,.2f}\n"
                                 f"Hodnocení: {valuation}")


    except ValueError as ve:
        result_text.delete(1.0, tkinter.END)
        result_text.insert(tkinter.END, f"Chyba: {ve}")
    except Exception as e:
        result_text.delete(1.0, tkinter.END)
        result_text.insert(tkinter.END, f"Nastala chyba: {e}")


# Nastavení fontů:
main_font = ("Arial", 10)
bold_font = ("Arial", 10, "bold")

# Vstupní pole pro zadávání údajů:
# TICKER:
label_ticker = Label(window, text="Ticker", bg="#127369", fg="#BFBFBF", font=bold_font)
label_ticker.grid(row=0, column=0)
ticker_entry = Entry(window, bg="#8AA6A3", font=main_font)
ticker_entry.grid(row=0, column=1, padx=10, pady=(10, 0.0))

# FREE CASH FLOW:
label_fcf = Label(window, text="FCF", bg="#127369", fg="#BFBFBF", font=bold_font)
label_fcf.grid(row=1, column=0)
fcf_entry = Entry(window, bg="#8AA6A3", font=main_font)
fcf_entry.grid(row=1, column=1, padx=10, pady=(10, 0.0))

# RŮSTOVÁ MÍRA:
label_growth = Label(window, text="Growth rate (%):", bg="#127369", fg="#BFBFBF", font=bold_font)
label_growth.grid(row=2, column=0)
growth_entry = Entry(window, bg="#8AA6A3", font=main_font)
growth_entry.insert(0, "5")  # Výchozí hodnota růstu
growth_entry.grid(row=2, column=1, padx=10, pady=(10, 0.0))

# DISKONTNÍ SAZBA:
label_discount = Label(window, text="Discount rate (%):", bg="#127369", fg="#BFBFBF", font=bold_font)
label_discount.grid(row=3, column=0)
discount_entry = Entry(window, bg="#8AA6A3", font=main_font)
discount_entry.insert(0, "10")  # Výchozí hodnota diskontní sazby
discount_entry.grid(row=3, column=1, padx=10, pady=(10, 0.0))

# POČET LET:
label_years = Label(window, text="Počet let:", bg="#127369", fg="#BFBFBF", font=bold_font)
label_years.grid(row=4, column=0)
years_entry = Entry(window, bg="#8AA6A3", font=main_font)
years_entry.insert(0, "10")  # Výchozí počet let
years_entry.grid(row=4, column=1, padx=10, pady=(10, 0.0))

# Tlačítko pro spuštění výpočtu:
calc_button = Button(window, text="Spočítej", bg="#10403B", fg="#BFBFBF", font=bold_font, command=calculate_and_display)
calc_button.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

# Výstupní label:
result_text = tkinter.Text(window, width=40, height=5, bg="#8AA6A3", font=main_font)
result_text.grid(row=6, column=0, columnspan=2, padx=10)

# Hlavní cyklus:
window.mainloop()