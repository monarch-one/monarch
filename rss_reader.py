#!/usr/bin/env python3
# Importación de bibliotecas necesarias
import curses  # Para interfaz TUI
import feedparser  # Para parsear feeds RSS
import webbrowser  # Para abrir enlaces en navegador
import time  # Para manejo de fechas
import textwrap  # Para ajustar texto
import os  # Para interactuar con el sistema de archivos
import json  # Para leer y guardar archivos JSON
import html  # Para des-escape de entidades HTML
import threading  # Para carga en segundo plano
from bs4 import BeautifulSoup  # Para limpiar contenido HTML

FEEDS = []  # Lista vacía que luego se llena con feeds personalizados

# Leer feeds adicionales desde custom_feeds.json si existe


def load_custom_feeds():
    custom_path = 'custom_feeds.json'
    if os.path.exists(custom_path):
        try:
            with open(custom_path, 'r', encoding='utf-8') as f:
                custom = json.load(f)
                return [(str(name), str(url)) for name, url in custom if isinstance(name, str) and isinstance(url, str)]
        except Exception:
            return []
    return []


# Carga inicial de feeds
FEEDS = load_custom_feeds()

# Inicializar variables globales
read_articles = set()  # Artículos leídos
favorites = []  # Lista de favoritos cargados
total_entries = []  # Lista completa para persistencia
entries = []  # Artículos cargados desde feeds
loading_done = False  # Bandera de carga completa
entries_loaded = 0  # Contador de feeds procesados

FAVORITES_FILE = 'favorites.json'  # Archivo para guardar favoritos

# Guardar favoritos en archivo JSON


def save_favorites():
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        json.dump([getattr(fav, 'link', '') for fav in favorites], f)

# Cargar favoritos desde archivo JSON


def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                links = set(json.load(f))
                return links
        except Exception:
            return set()
    return set()


# Inicializa el conjunto de enlaces favoritos
favorite_links = load_favorites()

# Función que corre en segundo plano para cargar artículos desde feeds


def fetch_entries_background(feed_list):
    import requests
    global entries_loaded
    all_entries = []
    for source_title, url in feed_list:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            for entry in feed.entries:
                entry.source_title = source_title
                all_entries.append(entry)
        except Exception:
            pass
        entries_loaded += 1
    all_entries.sort(key=lambda e: time.mktime(
        getattr(e, 'published_parsed', time.gmtime(0))), reverse=True)
    for entry in all_entries:
        if getattr(entry, 'link', None) in favorite_links:
            favorites.append(entry)
    entries.extend(all_entries)
    total_entries.extend(all_entries)
    global loading_done
    loading_done = True

# Añadir texto a pantalla de forma segura (sin romper)


def safe_addstr(stdscr, y, x, text, attr=0):
    max_y, max_x = stdscr.getmaxyx()
    if not (0 <= y < max_y) or x >= max_x:
        return
    safe_text = text[:max_x - x] if x < max_x else ""
    try:
        stdscr.addstr(y, x, safe_text, attr)
    except curses.error:
        pass

# Verifica si un artículo ya está marcado como favorito


def is_favorite(entry):
    link = getattr(entry, 'link', None)
    return any(getattr(fav, 'link', None) == link for fav in favorites)

# Dibuja una línea con el resumen de cada entrada RSS


def draw_entry(stdscr, y, entry, selected=False):
    date = time.strftime(
        '%Y-%m-%d', getattr(entry, 'published_parsed', time.gmtime(0)))
    source = getattr(entry, 'source_title', 'UNKNOWN')
    title = html.unescape(getattr(entry, 'title', 'No Title'))
    link = getattr(entry, 'link', None)

    max_y, max_x = stdscr.getmaxyx()
    separator = " | "
    space = len(date) + len(separator) + len(source) + len(separator) + 2
    available = max_x - space - 4
    title = title[:available] if available > 0 else ''

    attr = curses.A_REVERSE if selected else 0
    if link in read_articles:
        attr |= curses.color_pair(5) | curses.A_DIM

    x_offset = 2
    safe_addstr(stdscr, y, x_offset, date, attr)
    x_offset += len(date)
    safe_addstr(stdscr, y, x_offset, separator, attr)
    x_offset += len(separator)
    safe_addstr(stdscr, y, x_offset, source, attr | curses.color_pair(2))
    x_offset += len(source)
    safe_addstr(stdscr, y, x_offset, separator, attr)
    x_offset += len(separator)
    if is_favorite(entry):
        safe_addstr(stdscr, y, x_offset, '★ ', curses.color_pair(2) | attr)
        x_offset += 2
    safe_addstr(stdscr, y, x_offset, title, attr)

# Limpia HTML y presenta el contenido de forma legible


def format_html_content(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    parts = []
    images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
    links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
    for br in soup.find_all('br'):
        br.replace_with('\n')
    text = soup.get_text()

    if images:
        parts.append("Imágenes:")
        parts.extend([f"- {url}" for url in images])
    if links:
        parts.append("\nEnlaces:")
        parts.extend([f"- {url}" for url in links])
    if text:
        parts.append("\nContenido:")
        parts.append(text.strip())

    return "\n".join(parts)

# Dibuja la pantalla de artículos cargados


def draw_feed(stdscr, entries, idx):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    header = "★ MONARCH ★"
    safe_addstr(stdscr, 0, max(0, (max_x - len(header)) // 2),
                header, curses.A_BOLD | curses.color_pair(2))

    for i, entry in enumerate(entries):
        if i + 2 >= max_y - 2:
            break
        draw_entry(stdscr, i + 2, entry, selected=(i == idx))

    shortcuts = "j/J_k/K=PREV/NEXT | SPACE_BARR=READ | o/O=OPEN | s/S=SAVE | f/F=FAVORITES | q/Q=QUIT"
    safe_addstr(stdscr, max_y - 2, max(0, (max_x - len(shortcuts)) //
                2), shortcuts, curses.color_pair(1))
    stdscr.refresh()

# Muestra el contenido de un artículo seleccionado


def read_article(stdscr, entry):
    max_y, max_x = stdscr.getmaxyx()
    stdscr.clear()
    header = "★ MONARCH ★"
    centered_x = max(0, (max_x - len(header)) // 2)
    safe_addstr(stdscr, 0, centered_x, header,
                curses.A_BOLD | curses.color_pair(2))
    shortcuts = "j/J_k/K=PREV/NEXT | SPACE_BARR=READ | o/O=OPEN | s/S=SAVE | f/F=FAVORITES | q/Q=QUIT"
    safe_addstr(stdscr, max_y - 2, max(0, (max_x - len(shortcuts)) //
                2), shortcuts, curses.color_pair(1))

    title = html.unescape(getattr(entry, 'title', 'No Title'))
    date = html.unescape(
        getattr(entry, 'published', getattr(entry, 'updated', 'No Date')))
    raw_content = getattr(entry, 'summary', 'No content available')
    content = format_html_content(raw_content)
    source = getattr(entry, 'source_title', 'UNKNOWN')

    margin = 4
    text_width = max_x - 2 * margin
    safe_addstr(stdscr, 2, margin, source,
                curses.color_pair(2) | curses.A_BOLD)
    safe_addstr(stdscr, 3, margin, title, curses.color_pair(3) | curses.A_BOLD)
    safe_addstr(stdscr, 4, margin, date, curses.color_pair(4))

    lines = textwrap.wrap(content, text_width)
    for i, line in enumerate(lines[:max_y - 7]):
        safe_addstr(stdscr, i + 6, margin, line)

    stdscr.refresh()
    return 'waiting'

# Modo de visualización de favoritos


def favorites_mode(stdscr):
    idx = 0
    while True:
        draw_feed(stdscr, favorites, idx)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('j') and idx < len(favorites) - 1:
            idx += 1
        elif key == ord('k') and idx > 0:
            idx -= 1
        elif key == ord(' '):
            status = read_article(stdscr, favorites[idx])
            read_articles.add(getattr(favorites[idx], 'link', None))
            while True:
                key2 = stdscr.getch()
                if key2 in [ord('q'), ord('Q')]:
                    break
                elif key2 in [ord('j'), ord('J')] and idx < len(favorites) - 1:
                    idx += 1
                    status = read_article(stdscr, favorites[idx])
                    read_articles.add(getattr(favorites[idx], 'link', None))
                elif key2 in [ord('k'), ord('K')] and idx > 0:
                    idx -= 1
                    status = read_article(stdscr, favorites[idx])
                    read_articles.add(getattr(favorites[idx], 'link', None))
        elif key == ord('o'):
            webbrowser.open(getattr(favorites[idx], 'link', ''))

# Programa principal


def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

    thread = threading.Thread(
        target=fetch_entries_background, args=(FEEDS,), daemon=True)
    thread.start()

    idx = 0
    while not entries:
        time.sleep(0.1)

    while True:
        draw_feed(stdscr, entries, idx)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('j') and idx < len(entries) - 1:
            idx += 1
        elif key == ord('k') and idx > 0:
            idx -= 1
        elif key == ord(' '):
            if entries:
                status = read_article(stdscr, entries[idx])
                read_articles.add(getattr(entries[idx], 'link', None))
                while True:
                    key2 = stdscr.getch()
                    if key2 in [ord('q'), ord('Q')]:
                        break
                    elif key2 in [ord('j'), ord('J')] and idx < len(entries) - 1:
                        idx += 1
                        status = read_article(stdscr, entries[idx])
                        read_articles.add(getattr(entries[idx], 'link', None))
                    elif key2 in [ord('k'), ord('K')] and idx > 0:
                        idx -= 1
                        status = read_article(stdscr, entries[idx])
                        read_articles.add(getattr(entries[idx], 'link', None))
        elif key == ord('o') and entries:
            webbrowser.open(getattr(entries[idx], 'link', ''))
        elif key in [ord('s'), ord('l')] and entries:
            article = entries[idx]
            if all(getattr(article, 'link', None) != getattr(fav, 'link', None) for fav in favorites):
                favorites.append(article)
                save_favorites()
        elif key == ord('f'):
            favorites_mode(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)
