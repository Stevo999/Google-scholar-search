import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import webbrowser

def search_google_scholar(query):
    base_url = "https://scholar.google.com/scholar"
    params = {"q": query}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Process the search results here
        # For example, you can extract article titles, authors, links, etc.
        
        # Example: Get the titles and links of the search results
        results = soup.find_all("h3", class_="gs_rt")
        article_titles = []
        article_links = []
        
        for result in results:
            link = result.a
            if link:
                title = link.text
                link = link.get("href")
                article_titles.append(title)
                article_links.append(link)
        
        # Update the text widget with the search results
        result_text.delete("1.0", tk.END)  # Clear previous results
        if not article_titles:
            result_text.insert(tk.END, "No results found.")
        else:
            for i, (title, link) in enumerate(zip(article_titles, article_links), start=1):
                result_text.insert(tk.END, f"{i}. {title}\n", "link")
                result_text.tag_configure("link", foreground="blue", underline=True)
                result_text.tag_bind("link", "<Button-1>", lambda event, url=link: open_link(event, url))
        
    except requests.exceptions.RequestException as e:
        result_text.delete("1.0", tk.END)  # Clear previous results
        result_text.insert(tk.END, f"Error: {e}")

def open_link(event, link):
    webbrowser.open(link)

def search_button_clicked():
    query = entry.get()
    search_google_scholar(query)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Google Scholar Search")

    label = ttk.Label(root, text="Enter your search query:")
    label.pack()

    entry = ttk.Entry(root, width=50)
    entry.pack()

    search_button = ttk.Button(root, text="Search", command=search_button_clicked)
    search_button.pack()

    result_text = tk.Text(root, wrap=tk.WORD, width=80, height=20)
    result_text.pack()

    root.mainloop()
