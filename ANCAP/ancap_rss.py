#!/usr/bin/env python3
# Import necessary libraries
import curses # For TUI (Text-based User Interface)
import feedparser # For parsing RSS feeds (Really Simple Syndication)
import webbrowser # For opening links in web browser
import time # For date and time handling
import textwrap # For adjusting text to a specific width
import os # For interacting with the file system (e.g., checking files)
import json # For reading and saving JSON files (JavaScript Object Notation)
import html # For HTML entity unescaping (e.g., &amp; to &)
import threading # For background loading of feeds
import re # For regular expressions, used in text cleaning
import logging
import requests # For making HTTP requests
import concurrent.futures # For concurrent thread handling

# Define the base directory of this script to use absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Set up logging. Log file will be created in the logs directory
logging.basicConfig(filename=os.path.join(LOGS_DIR, 'ancap_rss.log'), level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
# For cleaning and parsing HTML content robustly
from bs4 import BeautifulSoup
# For internationalization (UI text translation)
import gettext

# Gettext configuration for internationalization
_ = gettext.gettext
try:
    # Associate the 'libertarian' domain with the 'locale' directory
    gettext.bindtextdomain('libertarian', 'locale')
    # Set 'libertarian' as the default domain
    gettext.textdomain('libertarian')
except Exception:
    # Ignore if gettext cannot be configured (e.g., on systems without full support)
    pass

SIDEBAR_WIDTH = 20 # Width dedicated to the command sidebar
HEADER_TOP_PADDING = 1

FEEDS = [] # Empty global list that is later filled with custom feeds

# Name of the file to save read article IDs/links
READ_FILE = os.path.join(DATA_DIR, 'read_articles.json')
# Name of the file to save favorite article links
FAVORITES_FILE = os.path.join(DATA_DIR, 'favorites.json')

# Read additional feeds from custom_feeds.json if it exists
def load_custom_feeds():
    # Path of the custom feeds configuration file
    custom_path = os.path.join(BASE_DIR, 'custom_feeds.json')
    if os.path.exists(custom_path): # Check if the file exists
        try:
            # Open the file in read mode with UTF-8 encoding
            with open(custom_path, 'r', encoding='utf-8') as f:
                custom = json.load(f) # Load the JSON content
                # Return a list of tuples (name, URL) ensuring both are strings
                return [(str(name), str(url)) for name, url in custom if isinstance(name, str) and isinstance(url, str)]
        # Catch any error during loading (e.g., malformed JSON)
        except Exception as e:
            logging.error(f"Error loading custom feeds from {custom_path}: {e}", exc_info=True)
            return [] # In case of error, return an empty list
    return [] # If the file doesn't exist, return an empty list

# Save read articles
def save_read_articles():
    # Open the read articles file in write mode
    with open(READ_FILE, 'w', encoding='utf-8') as f:
        # Save the set of read articles as a JSON list
        json.dump(list(read_articles), f)

# Load read articles
def load_read_articles():
    if os.path.exists(READ_FILE): # Check if the read articles file exists
        try:
            with open(READ_FILE, 'r', encoding='utf-8') as f: # Open the file in read mode
                # Load the JSON list and convert it to a set for efficient searches
                return set(json.load(f))
        except Exception as e: # Catch errors during loading
            logging.error(f"Error loading read articles from {READ_FILE}: {e}", exc_info=True)
            return set() # In case of error, return an empty set
    return set() # If the file doesn't exist, return an empty set

# Save favorites to JSON file
def save_favorites():
    # Open the favorites file in write mode
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        # Save only the links of favorite articles
        json.dump([getattr(fav, 'link', '') for fav in favorites], f)

# Load favorites from JSON file
def load_favorites():
    if os.path.exists(FAVORITES_FILE): # Check if the favorites file exists
        try:
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as f: # Open the file in read mode
                # Load the list of links and convert it to a set
                return set(json.load(f))
        except Exception as e: # Catch errors during loading
            logging.error(f"Error loading favorites from {FAVORITES_FILE}: {e}", exc_info=True)
            return set() # In case of error, return an empty set
    return set() # If the file doesn't exist, return an empty set


# Initial loading of feeds and favorites
FEEDS = load_custom_feeds() # Load custom feeds at program startup
# Load previously marked read articles
read_articles = load_read_articles()
favorites = [] # List to store favorite article objects in memory
# Load favorite article links for verification
favorite_links = load_favorites()
total_entries = [] # Global list that will contain all entries from all feeds
# Global list used to display entries (can be filtered/total)
entries = []
loading_done = False # Flag to indicate if feed loading is finished
entries_loaded = 0 # Counter to know how many feeds have been processed

problematic_feeds = []

# Function that runs in the background to load articles from feeds
def fetch_entries_background(feed_list):
    logging.debug('Starting fetch_entries_background.')
    global entries_loaded, loading_done, problematic_feeds
    all_entries = []
    
    def fetch_feed(session, source_title, url):
        try:
            logging.debug(f'Fetching feed: {source_title} from {url}')
            response = session.get(url, timeout=5)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            logging.debug(f'Fetched {len(feed.entries)} entries from {source_title}')
            fetched_entries = []
            for entry in feed.entries:
                entry.source_title = source_title
                fetched_entries.append(entry)
            return fetched_entries
        except Exception as e:
            logging.error(f"Error fetching feed for {source_title} from {url}: {e}", exc_info=True)
            problematic_feeds.append(f"{source_title}: {str(e)}")
            return []
    
    max_workers = min(10, len(feed_list)) if feed_list else 1
    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_feed = {executor.submit(fetch_feed, session, source_title, url): (source_title, url) for source_title, url in feed_list}
            for future in concurrent.futures.as_completed(future_to_feed):
                entries_from_feed = future.result()
                all_entries.extend(entries_from_feed)
                entries_loaded += 1
    
    all_entries.sort(key=lambda e: time.mktime(getattr(e, 'published_parsed', time.gmtime(0))), reverse=True)
    for entry in all_entries:
        if getattr(entry, 'link', None) in favorite_links:
            favorites.append(entry)
    favorites.sort(key=lambda e: time.mktime(getattr(e, 'published_parsed', time.gmtime(0))), reverse=True)
    
    entries.extend(all_entries)
    total_entries.extend(all_entries)
    loading_done = True
    logging.debug(f'fetch_entries_background completed. Total feeds processed: {entries_loaded}, total entries fetched: {len(all_entries)}')
    logging.debug(f'Total entries added to global list: {len(entries)}')

# Add text to screen safely (without breaking curses)
def safe_addstr(stdscr, y, x, text, attr=0):
    max_y, max_x = stdscr.getmaxyx() # Get the maximum dimensions of the window
    if not (0 <= y < max_y) or x >= max_x: # If the position is outside visible bounds
        return # Exit the function
    # Ensure that the text doesn't exceed the available width
    safe_text = str(text)
    if x + len(safe_text) > max_x:
        safe_text = safe_text[:max_x - x]
    
    try:
        # Try to add the string to the window with the given attributes
        stdscr.addstr(y, x, safe_text, attr)
    # Catch curses errors (e.g., if text is too long for remaining space)
    except curses.error:
        pass # Ignore the error and don't add the text

# Draw a line with the summary of each RSS entry
def draw_entry(stdscr, y, entry, selected=False, content_width=0, left_margin=2, right_margin=2):
    date = time.strftime('%d/%m/%Y', getattr(entry, 'published_parsed', time.gmtime(0)))
    source = f"[{getattr(entry, 'source_title', _('UNKNOWN')).lower()}]"
    title = html.unescape(getattr(entry, 'title', _('No Title')))
    link = getattr(entry, 'link', None)

    max_y, max_x = stdscr.getmaxyx()
    effective_max_x = content_width if content_width > 0 else (max_x - left_margin - right_margin)

    is_read = link in read_articles
    is_favorite = link in favorite_links
    if selected:
        attr = curses.color_pair(6)  # White for selected line
    elif is_read:
        attr = curses.color_pair(8)  # Gray for read articles
    else:
        attr = curses.color_pair(2)  # Yellow for unread articles

    # Render 'SAVED' at the left, yellow if favorite, gray if not
    saved_text = "SAVED"
    saved_color = curses.color_pair(2) if is_favorite else curses.color_pair(8)
    x_offset = left_margin
    safe_addstr(stdscr, y, x_offset, saved_text, saved_color)
    x_offset += len(saved_text) + 1

    # Render date
    safe_addstr(stdscr, y, x_offset, date, attr)
    x_offset += len(date) + 1

    # Render source
    safe_addstr(stdscr, y, x_offset, source, attr)
    x_offset += len(source) + 1

    # Calculate available space for title
    available = effective_max_x - x_offset - right_margin
    title = title[:available] if available > 0 else ''
    safe_addstr(stdscr, y, x_offset, title, attr)


# Clean HTML and present content in a readable way
def format_html_content(raw_html, text_width):
    # Remove script and style tags to avoid unwanted content
    soup = BeautifulSoup(raw_html, 'html.parser')
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # Replace <br> with newline for better readability
    for br in soup.find_all('br'):
        br.replace_with('\n')

    # Remove style attributes from all tags
    for tag in soup.find_all(True):
        if 'style' in tag.attrs:
            del tag.attrs['style']

    # Get text without style attributes
    # Use space as separator, and strip to clean extra whitespace
    text = soup.get_text(separator=' ', strip=True)
    
    # Replace multiple line breaks with a maximum of two (for paragraphs)
    # This will convert 3 or more \n into 2 \n (which will appear as a separate paragraph)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # This will ensure there are no whitespace before or after line breaks,
    # and that individual line breaks are handled as simple new lines
    text = re.sub(r'[ \t]*\n[ \t]*', '\n', text)
    
    # Remove multiple whitespace and spaces at the beginning/end of lines
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip() # Remove whitespace at the beginning/end of the complete text

    parts = []
    
    # Adjust text_width to ensure each line has a reasonable number of words
    # This will be the effective width for content
    dynamic_content_width = max(10, int(text_width)) # Use 100% of available width for content


    if text:
        paragraphs = text.split('\n\n') # Split by double line break to treat as paragraphs
        for i, para in enumerate(paragraphs):
            wrapped_para = textwrap.fill(
                para.strip(), width=dynamic_content_width, subsequent_indent="") 
            parts.extend([(line, curses.color_pair(6)) for line in wrapped_para.split('\n')])
            if i < len(paragraphs) - 1:
                parts.append(("", curses.color_pair(6)))
    else:
        parts.append((_("no content available."), curses.color_pair(6)))

    images = [img.get('src') for img in soup.find_all(
        'img') if img.get('src')]
    if images:
        parts.append(("", curses.color_pair(6)))
        for i, url in enumerate(images):
            wrapped_url = textwrap.fill(
                f"{i+1}. {url}", width=dynamic_content_width, subsequent_indent="  ")
            parts.extend([(line, curses.color_pair(6)) for line in wrapped_url.split('\n')])

    links = [a.get('href') for a in soup.find_all(
        'a') if a.get('href')]
    if links:
        parts.append(("", curses.color_pair(6)))
        for i, url in enumerate(links):
            wrapped_url = textwrap.fill(
                f"{i+1}. {url}", width=dynamic_content_width, subsequent_indent="  ")
            parts.extend([(line, curses.color_pair(6)) for line in wrapped_url.split('\n')])

    # Return a list of tuples (text line, attribute)
    return parts, dynamic_content_width


# Draw the loaded articles screen
def draw_feed(stdscr, entries, idx):
    stdscr.clear()
    LEFT_MARGIN = 2
    RIGHT_MARGIN = 2
    max_y, max_x = stdscr.getmaxyx()
    content_max_x = max_x - LEFT_MARGIN - RIGHT_MARGIN

    # Prominent ANCAP header with more readable ASCII art
    ancap_line1 = "▄▀█ █▄ █ █▀▀ ▄▀█ █▀█"
    ancap_line2 = "█▀█ █ ▀█ █▄▄ █▀█ █▀▀"
    subtitle = "» A LIBERTARIAN RSS READER «"
    
    # Center and display the ASCII logo
    safe_addstr(stdscr, HEADER_TOP_PADDING, LEFT_MARGIN + max(0, (content_max_x - len(ancap_line1)) // 2), ancap_line1, curses.color_pair(2))
    safe_addstr(stdscr, HEADER_TOP_PADDING + 1, LEFT_MARGIN + max(0, (content_max_x - len(ancap_line2)) // 2), ancap_line2, curses.color_pair(2))
    safe_addstr(stdscr, HEADER_TOP_PADDING + 2, LEFT_MARGIN + max(0, (content_max_x - len(subtitle)) // 2), subtitle, curses.color_pair(6))
    
    # Line 1: Main statistics (centered)
    unread_count = len([e for e in entries if getattr(e, 'link', None) not in read_articles])
    total_count = len(entries)
    feeds_count = len(FEEDS)
    
    stats_line = f"ARTICLES: {total_count} | UNREAD: {unread_count} | FEEDS: {feeds_count}"
    if favorites:
        stats_line += f" | FAVORITES: {len(favorites)}"
    
    stats_y = HEADER_TOP_PADDING + 4  # Adjust for the new more compact header
    stats_x = LEFT_MARGIN + max(0, (content_max_x - len(stats_line)) // 2)
    safe_addstr(stdscr, stats_y, stats_x, stats_line, curses.color_pair(2))
    
    # Line 2: Status and date/time (aligned to extremes)
    status_y = HEADER_TOP_PADDING + 5  # Adjust for the new more compact header
    
    # System status (left)
    status_parts = []
    if problematic_feeds:
        status_parts.append(f"⚠ {len(problematic_feeds)} feeds with issues")
    if loading_done:
        status_parts.append("✓ UPDATED")
    else:
        status_parts.append("⟳ updating...")
    
    status_text = " | ".join(status_parts)
    
    # Show status with different colors
    if loading_done:
        safe_addstr(stdscr, status_y, LEFT_MARGIN, status_text, curses.color_pair(2))  # Yellow for updated
    else:
        safe_addstr(stdscr, status_y, LEFT_MARGIN, status_text, curses.color_pair(7))  # Gray for updating
    
    # Date and time (right)
    current_time = time.strftime('%H:%M:%S')
    current_date = time.strftime('%d/%m/%Y')
    datetime_text = f"{current_date} {current_time}"
    datetime_x = LEFT_MARGIN + content_max_x - len(datetime_text)
    safe_addstr(stdscr, status_y, datetime_x, datetime_text, curses.color_pair(2))

    # Blank line for separation
    blank_y = status_y + 1
    safe_addstr(stdscr, blank_y, LEFT_MARGIN, " " * content_max_x, curses.color_pair(2))

    # Calculate available area for articles
    header_height = status_y + 2  # Adjusted complete header height
    footer_height = 3  # Space reserved for shortcuts in the footer
    display_height = max_y - header_height - footer_height
    start_display_row = header_height

    if len(entries) > display_height:
        start = max(0, idx - display_height // 2)
        start = min(start, len(entries) - display_height)
    else:
        start = 0

    end = min(len(entries), start + display_height)

    for i, entry in enumerate(entries[start:end], start=start):
        draw_entry(stdscr, start_display_row + i - start, entry,
                   selected=(i == idx), content_width=content_max_x, left_margin=LEFT_MARGIN, right_margin=RIGHT_MARGIN)

    # Shortcuts at the bottom (footer) - single line
    footer_y = max_y - 2
    
    # Yellow separator line
    separator = "─" * content_max_x
    safe_addstr(stdscr, footer_y, LEFT_MARGIN, separator, curses.color_pair(2))
    
    # All shortcuts on a single line (all yellow)
    shortcuts_text = "j/k=nav SPACE=read o=open f=fav l=save u=unread m=mark all q/ESC=exit PgUp/PgDn=scroll"
    
    # Center the shortcuts
    start_x = LEFT_MARGIN + max(0, (content_max_x - len(shortcuts_text)) // 2)
    safe_addstr(stdscr, footer_y + 1, start_x, shortcuts_text, curses.color_pair(2))

    stdscr.refresh()

# Display the content of a selected article
def read_article(stdscr, current_entries_list, initial_idx):
    current_idx = initial_idx # Maintain a local index for J/K navigation

    # Mark the current article as read when entering reading mode
    current_link = getattr(current_entries_list[current_idx], 'link', None)
    if current_link:
        read_articles.add(current_link)
        save_read_articles()

    current_line_offset = 0 # Offset for content line scrolling
    # We remove link navigation: j/k only change articles

    LEFT_MARGIN = 20  # Increased margin for more separation
    RIGHT_MARGIN = 20

    while True: # Loop for reading mode (allows J/K navigation)
        # Get the current article according to the index
        entry = current_entries_list[current_idx]

        max_y, max_x = stdscr.getmaxyx() # Get window dimensions
        stdscr.clear() # Clear the screen
        
        # Calculate content area width
        content_max_x = max_x - LEFT_MARGIN - RIGHT_MARGIN

        # Prominent ANCAP header with more readable ASCII art
        ancap_line1 = "▄▀█ █▄ █ █▀▀ ▄▀█ █▀█"
        ancap_line2 = "█▀█ █ ▀█ █▄▄ █▀█ █▀▀"
        subtitle = "» A LIBERTARIAN RSS READER «"
        
        # Center and display the ASCII logo
        safe_addstr(stdscr, HEADER_TOP_PADDING, LEFT_MARGIN + max(0, (content_max_x - len(ancap_line1)) // 2), ancap_line1, curses.color_pair(2))
        safe_addstr(stdscr, HEADER_TOP_PADDING + 1, LEFT_MARGIN + max(0, (content_max_x - len(ancap_line2)) // 2), ancap_line2, curses.color_pair(2))
        safe_addstr(stdscr, HEADER_TOP_PADDING + 2, LEFT_MARGIN + max(0, (content_max_x - len(subtitle)) // 2), subtitle, curses.color_pair(6))

        # Article title (unescaped and translatable)
        title = html.unescape(getattr(entry, 'title', _('No Title')))
        # Use published_parsed for local date/time formatting if available
        published_parsed = getattr(entry, 'published_parsed', None)
        if published_parsed:
            date = time.strftime('%d/%m/%Y %H:%M', published_parsed)
        else:
            date = html.unescape(getattr(entry, 'published', getattr(entry, 'updated', _('No Date'))))
        raw_content = getattr(entry, 'summary', _('No content available'))

        # Responsive width for content
        content_text_width_for_func = content_max_x
        formatted_content_parts, actual_content_width = format_html_content(raw_content, content_text_width_for_func)
        # Find all links in the article content
        soup = BeautifulSoup(raw_content, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a') if a.get('href')]





        # Move title to sources position, in white and separated from text by an empty line
        # Calculate available width for title leaving space for SAVED
        saved_text = "SAVED"
        title_width = actual_content_width - len(saved_text) - 3  # 3 space margin
        wrapped_title_lines = textwrap.fill(title, width=title_width).split('\n')
        title_start_line = HEADER_TOP_PADDING + 4  # Adjusted to start after header
        
        # Check if current article is favorite for SAVED indicator
        current_article_link = getattr(entry, 'link', None)
        is_current_favorite = current_article_link in favorite_links
        
        for i, line in enumerate(wrapped_title_lines):
            safe_addstr(stdscr, title_start_line + i, LEFT_MARGIN, line, curses.color_pair(6))  # White
            
            # Render SAVED on the first line of the title, aligned to the right
            if i == 0:
                saved_color = curses.color_pair(2) if is_current_favorite else curses.color_pair(8)
                saved_x_position = LEFT_MARGIN + content_max_x - len(saved_text)
                safe_addstr(stdscr, title_start_line + i, saved_x_position, saved_text, saved_color)

        # Empty line below title
        blank_line_y = title_start_line + len(wrapped_title_lines)  
        safe_addstr(stdscr, blank_line_y, LEFT_MARGIN, "", curses.color_pair(2))

        # Show sources in yellow, lowercase and in brackets
        source = f"[{getattr(entry, 'source_title', _('UNKNOWN')).lower()}]"
        source_attr = curses.color_pair(2)  # Yellow
        source_y = blank_line_y + 1
        
        # Calculate date and time to determine available space
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%d/%m/%Y')
        datetime_text = f"{current_date} {current_time}"
        
        # Render source on the left (truncated if necessary to avoid overlap)
        max_source_width = content_max_x - len(datetime_text) - 3  # 3 space margin
        if len(source) > max_source_width:
            source = source[:max_source_width - 3] + "..."
        safe_addstr(stdscr, source_y, LEFT_MARGIN, source, source_attr)
        
        # Render date and time on the same line as source, aligned to the right
        datetime_x_position = LEFT_MARGIN + content_max_x - len(datetime_text)
        safe_addstr(stdscr, source_y, datetime_x_position, datetime_text, curses.color_pair(2))

        # Insert a blank line below the date for visual separation
        blank_line_y = source_y + 1
        safe_addstr(stdscr, blank_line_y, LEFT_MARGIN, "", curses.color_pair(2))

        # Content lines, left-aligned
        content_start_line = blank_line_y + 1
        display_height_for_content = max_y - content_start_line - 1
        # Show content without link navigation
        lines_with_attr = [(line, curses.color_pair(2)) for line, _ in formatted_content_parts]
        display_lines_with_attr = lines_with_attr[current_line_offset: current_line_offset + display_height_for_content]
        for i, (line, attr) in enumerate(display_lines_with_attr):
            line_y = content_start_line + i
            safe_addstr(stdscr, line_y, LEFT_MARGIN, line, attr)
        
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord(' '):
            return current_idx
        elif key == ord('o'):
            webbrowser.open(getattr(entry, 'link', ''))
        elif key == ord('t') or key == ord('T'):
            pass
        elif key == ord('u'):
            link_to_unmark = getattr(current_entries_list[current_idx], 'link', None)
            if link_to_unmark in read_articles:
                read_articles.remove(link_to_unmark)
                save_read_articles()
            stdscr.clear()
            continue
        elif key == ord('m'): # 'm' to toggle mark all as read/unread
            # Count read and unread articles
            read_count = sum(1 for entry in current_entries_list if getattr(entry, 'link', None) in read_articles)
            unread_count = len(current_entries_list) - read_count
            
            # If there are more unread than read, mark all as read
            # If there are more read than unread, mark all as unread
            if unread_count >= read_count:
                # Mark all as read
                for entry in current_entries_list:
                    entry_link = getattr(entry, 'link', None)
                    if entry_link:
                        read_articles.add(entry_link)
            else:
                # Mark all as unread
                for entry in current_entries_list:
                    entry_link = getattr(entry, 'link', None)
                    if entry_link and entry_link in read_articles:
                        read_articles.remove(entry_link)
            save_read_articles()
            stdscr.clear()
            continue
        elif key in [ord('s'), ord('l')]: # 's' or 'l' to save/mark as favorite (toggle)
            article = current_entries_list[current_idx]
            link_to_toggle = getattr(article, 'link', None)
            if link_to_toggle in favorite_links: # If already favorite, remove it
                favorites[:] = [fav for fav in favorites if getattr(fav, 'link', None) != link_to_toggle]
                favorite_links.remove(link_to_toggle)
            else: # If not favorite, add it
                favorites.append(article)
                favorite_links.add(link_to_toggle)
            # Re-sort favorites list after adding/removing
            favorites.sort(key=lambda e: time.mktime(getattr(e, 'published_parsed', time.gmtime(0))), reverse=True)
            save_favorites() # Save favorites
        elif key == ord('j') or key == curses.KEY_DOWN:
            if current_idx < len(current_entries_list) - 1:
                current_idx += 1
                current_line_offset = 0
                read_articles.add(getattr(current_entries_list[current_idx], 'link', None))
                save_read_articles()
            else:
                current_idx = 0
                current_line_offset = 0
                read_articles.add(getattr(current_entries_list[current_idx], 'link', None))
                save_read_articles()
        elif key == ord('k') or key == curses.KEY_UP:
            if current_idx > 0:
                current_idx -= 1
                current_line_offset = 0
                read_articles.add(getattr(current_entries_list[current_idx], 'link', None))
                save_read_articles()
            else:
                current_idx = len(current_entries_list) - 1
                current_line_offset = 0
                read_articles.add(getattr(current_entries_list[current_idx], 'link', None))
                save_read_articles()
        elif key == curses.KEY_NPAGE:
            current_line_offset = min(
                current_line_offset + display_height_for_content, len(lines_with_attr) - display_height_for_content)
            current_line_offset = max(0, current_line_offset)
        elif key == curses.KEY_PPAGE:
            current_line_offset = max(
                0, current_line_offset - display_height_for_content)
        elif key == curses.KEY_MOUSE:
            try:
                id, x, y, z, bstate = curses.getmouse()
                if bstate & curses.BUTTON4_PRESSED:
                    current_line_offset = max(
                        0, current_line_offset - 3)
                elif bstate & curses.BUTTON5_PRESSED:
                    current_line_offset = min(
                        current_line_offset + 3, len(lines_with_attr) - display_height_for_content)
                    current_line_offset = max(0, current_line_offset)
            except curses.error:
                pass


# Favorites display mode
def favorites_mode(stdscr):
    idx = 0 # Index of selected article
    # If there are no favorites, don't enter the loop
    if not favorites:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        # Prominent ANCAP header with more readable ASCII art
        ancap_line1 = "▄▀█ █▄ █ █▀▀ ▄▀█ █▀█"
        ancap_line2 = "█▀█ █ ▀█ █▄▄ █▀█ █▀▀"
        subtitle = "» A LIBERTARIAN RSS READER «"
        
        # Center and display the ASCII logo
        header_start_y = max_y // 2 - 6
        safe_addstr(stdscr, header_start_y, max(0, (max_x - len(ancap_line1)) // 2), ancap_line1, curses.color_pair(2))
        safe_addstr(stdscr, header_start_y + 1, max(0, (max_x - len(ancap_line2)) // 2), ancap_line2, curses.color_pair(2))
        safe_addstr(stdscr, header_start_y + 2, max(0, (max_x - len(subtitle)) // 2), subtitle, curses.color_pair(6))
        
        safe_addstr(stdscr, max_y // 2 + 1, max(0, (max_x - len(_("no favorites yet.")))) // 2),
        _("no favorites yet."), curses.color_pair(2) # No favorites message in yellow
        safe_addstr(stdscr, max_y // 2 + 2, max(0, (max_x - len(_("press any key to return."))) // 2),
        _("press any key to return."), curses.color_pair(2)) # Return message in yellow
        stdscr.refresh()
        stdscr.getch() # Wait for a key to return
        return

    while True:
        draw_feed(stdscr, favorites, idx) # Draw the favorites list
        key = stdscr.getch()
        # Inside read_article function, after key = stdscr.getch()
        stdscr.refresh() # Wait for user input
        if key == ord('q') or key == 27: # 'q' or ESC to exit favorites mode
            break
        # 'j' or down arrow for next article
        elif key == ord('j') or key == curses.KEY_DOWN:
            if idx < len(favorites) - 1:
                idx += 1
        # 'k' or up arrow for previous article
        elif key == ord('k') or key == curses.KEY_UP:
            if idx > 0:
                idx -= 1
        elif key == ord(' '): # Space to read selected article
            returned_idx = read_article(stdscr, favorites, idx)
            idx = returned_idx # Update index after reading
            # Already marked as read inside read_article when entering
            # read_articles.add(getattr(favorites[idx], 'link', None))
            # save_read_articles() # Save read articles
        elif key == ord('o') or key == 10: # 'o' or Enter to open article
            webbrowser.open(getattr(favorites[idx], 'link', ''))
        # 's' or 'l' to save/mark as favorite (toggle)
        elif key in [ord('s'), ord('l')] and entries: # 's' or 'l' to save/mark as favorite (toggle)
            article = favorites[idx]
            link_to_toggle = getattr(article, 'link', None)
            if link_to_toggle in favorite_links: # If already favorite, remove it
                favorites[:] = [fav for fav in favorites if getattr(fav, 'link', None) != link_to_toggle]
                favorite_links.remove(link_to_toggle)
            else: # If not favorite, add it
                favorites.append(article)
                favorite_links.add(link_to_toggle)
            # Re-sort favorites list after adding/removing
            favorites.sort(key=lambda e: time.mktime(getattr(e, 'published_parsed', time.gmtime(0))), reverse=True)
            save_favorites() # Save favorites
            # Adjust index if last element was removed
            if idx >= len(favorites) and len(favorites) > 0:
                idx = len(favorites) - 1
            elif len(favorites) == 0: # If no favorites remain, exit mode
                break
        # 'u' to mark as unread
        elif key == ord('u'):
            link_to_unmark = getattr(favorites[idx], 'link', None)
            if link_to_unmark in read_articles:
                read_articles.remove(link_to_unmark)
                save_read_articles()
            # Redraw screen so article color changes
            # No `continue` here because favorites_mode calls draw_feed again in each iteration
        elif key == ord('m'): # 'm' to toggle mark all favorites as read/unread
            # Count read and unread favorites
            read_count = sum(1 for fav in favorites if getattr(fav, 'link', None) in read_articles)
            unread_count = len(favorites) - read_count
            
            # If there are more unread than read, mark all as read
            # If there are more read than unread, mark all as unread
            if unread_count >= read_count:
                # Mark all favorites as read
                for fav in favorites:
                    fav_link = getattr(fav, 'link', None)
                    if fav_link:
                        read_articles.add(fav_link)
            else:
                # Mark all favorites as unread
                for fav in favorites:
                    fav_link = getattr(fav, 'link', None)
                    if fav_link and fav_link in read_articles:
                        read_articles.remove(fav_link)
            save_read_articles()
        elif key == curses.KEY_MOUSE: # If mouse event is detected
            try:
                # Get mouse event details
                id, x, y, z, bstate = curses.getmouse()
                # Mouse wheel up (scroll up)
                if bstate & curses.BUTTON4_PRESSED: # Left mouse button clicked
                    # Calculate visible start on screen
                    display_height = max_y - 7 # Adjusted to leave an extra blank line
                    start_display_row = 3
                    if len(favorites) > display_height:
                        current_screen_start_idx = max(
                            0, idx - display_height // 2)
                        current_screen_start_idx = min(
                            current_screen_start_idx, len(favorites) - display_height)
                    else:
                        current_screen_start_idx = 0

                    # If click is within visible article list
                    if y >= start_display_row and y < start_display_row + display_height:
                        clicked_idx_on_screen = y - start_display_row # Calculate relative screen index
                        clicked_absolute_idx = current_screen_start_idx + clicked_idx_on_screen
                        
                        if clicked_absolute_idx < len(favorites):
                            returned_idx = read_article(stdscr, favorites, clicked_absolute_idx)
                            idx = returned_idx # Update index
                            # Already marked as read inside read_article when entering
                            # read_articles.add(getattr(favorites[idx], 'link', None))
                            # save_read_articles()
                elif bstate & curses.BUTTON4_PRESSED: # Mouse wheel up (scroll up)
                    if idx > 0:
                        idx -= 1
                elif bstate & curses.BUTTON5_PRESSED: # Mouse wheel down (scroll down)
                    if idx < len(favorites) - 1:
                        idx += 1
            except curses.error:
                pass # Ignore mouse errors

# Main program
def main(stdscr):
    stdscr.clear() # Clear the screen
    curses.curs_set(0) # Hide the cursor
    curses.start_color() # Start curses color system
    
    # Initialize color pairs
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow
    curses.init_pair(6, 255, curses.COLOR_BLACK)  # Pure white
    curses.init_pair(7, 248, curses.COLOR_BLACK)  # Light gray
    curses.init_pair(8, 8, curses.COLOR_BLACK)    # Dark gray

    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION) # Enable all mouse events and position tracking

    global entries  # Declare entries as global to ensure it is accessible
    entries = []  # Initialize entries as an empty list

    logging.debug(f"FEEDS loaded: {FEEDS}")
    logging.debug("Starting thread for fetch_entries_background.")
    thread = threading.Thread(
        target=fetch_entries_background, args=(FEEDS,), daemon=True)
    thread.start()
    logging.debug("Thread started.")

    idx = 0

    while not entries and thread.is_alive():
        logging.debug(f"Entries still empty. Thread alive: {thread.is_alive()}")
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        # Prominent ANCAP header with more readable ASCII art
        ancap_line1 = "▄▀█ █▄ █ █▀▀ ▄▀█ █▀█"
        ancap_line2 = "█▀█ █ ▀█ █▄▄ █▀█ █▀▀"
        subtitle = "» A LIBERTARIAN RSS READER «"
        
        # Center and display the ASCII logo
        header_start_y = max_y // 2 - 8
        safe_addstr(stdscr, header_start_y, max(0, (max_x - len(ancap_line1)) // 2), ancap_line1, curses.color_pair(2))
        safe_addstr(stdscr, header_start_y + 1, max(0, (max_x - len(ancap_line2)) // 2), ancap_line2, curses.color_pair(2))
        safe_addstr(stdscr, header_start_y + 2, max(0, (max_x - len(subtitle)) // 2), subtitle, curses.color_pair(6))
        
        # Blank line
        safe_addstr(stdscr, header_start_y + 3, 0, "")

        loading_message = _("loading feeds... please wait") # Loading message (translatable)
        safe_addstr(stdscr, max_y // 2 - 1, max(0, (max_x - len(loading_message)) // 2),
                    loading_message, curses.color_pair(2)) # In yellow

        # Progress bar
        total_feeds = len(FEEDS) 
        if total_feeds == 0: # Empty feeds case, to avoid division by zero
            progress_percent = 0
        else:
            progress_percent = int((entries_loaded / total_feeds) * 100)
        
        bar_length = max_x - 20 # Progress bar length
        if bar_length < 0: bar_length = 0 # Ensure it's not negative
        
        filled_length = int(bar_length * progress_percent / 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        progress_text = f"[{bar}] {progress_percent}%"
        safe_addstr(stdscr, max_y // 2 + 1, max(0, (max_x - len(progress_text)) // 2),
                    progress_text, curses.color_pair(2)) # In yellow

        stdscr.refresh()
        # Display problematic feeds if any
        if problematic_feeds:
            error_message = "Feeds with issues: " + ", ".join(problematic_feeds)
            # Truncate message if too long
            if len(error_message) > max_x - 4:
                error_message = error_message[:max_x - 7] + "..."
            safe_addstr(stdscr, max_y // 2 + 3, max(0, (max_x - len(error_message)) // 2), error_message, curses.color_pair(7))
        time.sleep(0.1) # Wait a bit before checking again

    if not entries and not thread.is_alive(): # If no entries loaded and thread finished
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        # Prominent ANCAP header with more readable ASCII art
        ancap_line1 = "▄▀█ █▄ █ █▀▀ ▄▀█ █▀█"
        ancap_line2 = "█▀█ █ ▀█ █▄▄ █▀█ █▀▀"
        subtitle = "» A LIBERTARIAN RSS READER «"
        
        # Center and display the ASCII logo
        header_start_y = max_y // 2 - 6
        safe_addstr(stdscr, header_start_y, max(0, (max_x - len(ancap_line1)) // 2), ancap_line1, curses.color_pair(2))
        safe_addstr(stdscr, header_start_y + 1, max(0, (max_x - len(ancap_line2)) // 2), ancap_line2, curses.color_pair(2))
        safe_addstr(stdscr, header_start_y + 2, max(0, (max_x - len(subtitle)) // 2), subtitle, curses.color_pair(6))
        
        no_feeds_message = _("NO FEEDS LOADED OR CUSTOM_FEEDS.JSON IS EMPTY/INVALID.").upper() # Error message (translatable)
        safe_addstr(stdscr, max_y // 2 + 1, max(0, (max_x - len(no_feeds_message)) // 2),
                    no_feeds_message, curses.color_pair(2)) # In yellow
        safe_addstr(stdscr, max_y // 2 + 2, max(0, (max_x - len(_("PRESS ANY KEY TO EXIT.").upper())) // 2),
                    _("PRESS ANY KEY TO EXIT.").upper(), curses.color_pair(2)) # In yellow
        stdscr.refresh()
        stdscr.getch()
        return # Exit the program

    while True: # Main interface loop
        draw_feed(stdscr, entries, idx) # Draw the main feeds screen
        
        # Set a timeout so the screen refreshes every 30 seconds to update time
        stdscr.timeout(30000)  # 30 seconds timeout
        key = stdscr.getch() # Wait for user input (keyboard or mouse)
        stdscr.timeout(-1)  # Reset to blocking mode
        
        # If timeout occurred (key == -1), just redraw the screen
        if key == -1:
            continue
            
        if key == ord('q') or key == 27: # 'q' or ESC to exit the program
            break
        elif key == ord('j') or key == curses.KEY_DOWN: # 'j' or down arrow for next article
            if idx < len(entries) - 1:
                idx += 1
        elif key == ord('k') or key == curses.KEY_UP: # 'k' or up arrow for previous article
            if idx > 0:
                idx -= 1
        elif key == ord(' '): # Space to read selected article
            if entries: # Ensure there are articles to read
                returned_idx = read_article(stdscr, entries, idx) # Pass the list and index
                idx = returned_idx # Update main index with returned one
                # Marking as read is already done inside read_article when entering
                # read_articles.add(getattr(entries[idx], 'link', None))
                # save_read_articles() # Save read articles changes
        elif key == ord('o') and entries:
            webbrowser.open(getattr(entries[idx], 'link', ''))
        elif key in [ord('s'), ord('l')] and entries: # 's' or 'l' to save/mark as favorite (toggle)
            article = entries[idx]
            link_to_toggle = getattr(article, 'link', None)
            if link_to_toggle in favorite_links: # If already favorite, remove it
                favorites[:] = [fav for fav in favorites if getattr(fav, 'link', None) != link_to_toggle]
                favorite_links.remove(link_to_toggle)
            else: # If not favorite, add it
                favorites.append(article)
                favorite_links.add(link_to_toggle)
            # Re-sort favorites list after adding/removing
            favorites.sort(key=lambda e: time.mktime(getattr(e, 'published_parsed', time.gmtime(0))), reverse=True)
            save_favorites() # Save favorites
        elif key == ord('u') and entries: # 'u' to mark as unread
            link_to_unmark = getattr(entries[idx], 'link', None)
            if link_to_unmark in read_articles:
                read_articles.remove(link_to_unmark)
                save_read_articles()
            # No need for `stdscr.clear()` here because `draw_feed` handles that.
            # Simply update state and redraw in next main loop iteration.
        elif key == ord('m') and entries: # 'm' to toggle mark all as read/unread
            # Count read and unread articles
            read_count = sum(1 for entry in entries if getattr(entry, 'link', None) in read_articles)
            unread_count = len(entries) - read_count
            
            # If there are more unread than read, mark all as read
            # If there are more read than unread, mark all as unread
            if unread_count >= read_count:
                # Mark all as read
                for entry in entries:
                    entry_link = getattr(entry, 'link', None)
                    if entry_link:
                        read_articles.add(entry_link)
            else:
                # Mark all as unread
                for entry in entries:
                    entry_link = getattr(entry, 'link', None)
                    if entry_link and entry_link in read_articles:
                        read_articles.remove(entry_link)
            save_read_articles()
        elif key == ord('f'): # 'f' to enter favorites mode
            favorites_mode(stdscr)
        elif key == ord('t') or key == ord('T'): # 't' or 'T' to translate (functionality pending integration with external API)
            pass
        elif key == curses.KEY_NPAGE: # Page Down key to advance one page in the list
            num_display_lines = max_y - 7 # Space for articles (adjusted for new height calculation)
            idx = min(idx + num_display_lines, len(entries) - 1) # Advance the index
        elif key == curses.KEY_PPAGE: # Page Up key to go back one page in the list
            num_display_lines = max_y - 7
            idx = max(0, idx - num_display_lines) # Go back the index
        elif key == curses.KEY_MOUSE: # If mouse event is detected
            try:
                # Get mouse event details
                id, x, y, z, bstate = curses.getmouse()
                
                # Mouse wheel up (scroll up)
                if bstate & curses.BUTTON4_PRESSED:
                    if idx > 0:
                        idx -= 1
                # Mouse wheel down (scroll down)
                elif bstate & curses.BUTTON5_PRESSED:
                    if idx < len(entries) - 1:
                        idx += 1
                elif bstate & curses.BUTTON1_PRESSED: # Left mouse button clicked
                    # Calculate visible start on screen
                    display_height = max_y - 7 # Height available for articles
                    start_display_row = 3 # Row where articles start
                    
                    if len(entries) > display_height:
                        # Ensure current_screen_start_idx is not negative
                        current_screen_start_idx = max(0, idx - display_height // 2)
                        # Ensure it doesn't exceed the end of the list
                        current_screen_start_idx = min(current_screen_start_idx, len(entries) - display_height)
                    else:
                        current_screen_start_idx = 0

                    # Make sure the click is within the articles area
                    if y >= start_display_row and y < start_display_row + display_height:
                        clicked_idx_on_screen = y - start_display_row # Calculate relative screen index
                        clicked_absolute_idx = current_screen_start_idx + clicked_idx_on_screen
                        
                        if clicked_absolute_idx < len(entries): # Ensure index is valid
                            idx = clicked_absolute_idx # Update selected index
                            # Now we open the article on click
                            returned_idx = read_article(stdscr, entries, idx)
                            idx = returned_idx # Update main index with returned one
                            # Marking as read is already done inside read_article when entering
                            # read_articles.add(getattr(entries[idx], 'link', None))
                            # save_read_articles()
            except curses.error:
                pass # Ignore mouse errors

if __name__ == "__main__":
    curses.wrapper(main)