import requests
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

# Replace 'YOUR_API_KEY' with your actual API key from NewsAPI
API_KEY = '4d1fa4a0c5f946e39ab364211eb3c82b'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'


def fetch_news(category):
    params = {
        'apiKey': API_KEY,
        'category': category,
        'country': 'us'
    }
    response = requests.get(NEWS_API_URL, params=params)
    news_data = response.json()

    if news_data.get('status') == 'ok':
        articles = news_data.get('articles', [])
        return articles
    else:
        return []


def display_news():
    category = news_category.get()
    news_articles = fetch_news(category)

    for widget in news_frame.winfo_children():
        widget.destroy()

    if news_articles:
        for article in news_articles:
            frame = ttk.Frame(news_frame, style='News.TFrame')
            frame.pack(fill=tk.X, pady=10)

            text_frame = ttk.Frame(frame, style='Text.TFrame')
            text_frame.pack(fill=tk.X, expand=True)

            title_label = ttk.Label(text_frame, text=article['title'], style='Title.TLabel', wraplength=700)
            title_label.pack(anchor=tk.W, padx=10)

            desc_label = ttk.Label(text_frame, text=article['description'], style='Description.TLabel', wraplength=700)
            desc_label.pack(anchor=tk.W, padx=10, pady=5)

            url_label = ttk.Label(text_frame, text=article['url'], style='URL.TLabel', wraplength=700)
            url_label.pack(anchor=tk.W, padx=10)

            animate_label(title_label)
            animate_label(desc_label)
            animate_label(url_label)

    news_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def animate_label(label):
    label.after(0, fade_in, label, 0)


def fade_in(label, alpha):
    alpha += 0.05
    label.config(foreground=f'#{int(255 * alpha):02x}{255:02x}{int(255 * alpha):02x}')
    if alpha < 1.0:
        label.after(50, fade_in, label, alpha)


# Setting up the Tkinter window with themes
root = ThemedTk(theme="breeze")
root.title("Daily News Fetcher")
root.geometry('1000x800')

# Styles
style = ttk.Style()
style.configure('News.TFrame', background='#2e3f4f')
style.configure('Text.TFrame', background='#2e3f4f')
style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'), background='#2e3f4f', foreground='white')
style.configure('Description.TLabel', font=('Helvetica', 10), background='#2e3f4f', foreground='lightgray')
style.configure('URL.TLabel', font=('Helvetica', 10, 'italic'), background='#2e3f4f', foreground='#1e90ff')

# Drop-down menu for news categories
categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
news_category = ttk.Combobox(root, values=categories, style='TCombobox')
news_category.set("Select a category")
news_category.grid(column=0, row=0, padx=10, pady=10)

# Button to fetch news
fetch_button = ttk.Button(root, text="Fetch News", command=display_news, style='TButton')
fetch_button.grid(column=1, row=0, padx=10, pady=10)

# Frame to hold the news articles
frame_container = ttk.Frame(root, style='News.TFrame')
frame_container.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="nsew")

canvas = tk.Canvas(frame_container, background='#2e3f4f')
scrollbar = ttk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
news_frame = ttk.Frame(canvas, style='News.TFrame')

news_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=news_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Configure the grid to expand properly
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
frame_container.columnconfigure(0, weight=1)
frame_container.rowconfigure(0, weight=1)

root.mainloop()
