import curses
import feedparser
import webbrowser
import time

# Global set to track read articles (using their link as identifier)
read_articles = set()

# Replace this with your desired RSS feed URL
FEED_URL = 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'


def fetch_and_sort_entries(feed_url):
    feed = feedparser.parse(feed_url)
    # Sort entries by published date (most recent first)
    entries = sorted(feed.entries, key=lambda e: time.mktime(e.published_parsed) if hasattr(e, 'published_parsed') else 0, reverse=True)
    return entries


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(0)   # Wait for user input
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.clear()

    entries = fetch_and_sort_entries(FEED_URL)
    if not entries:
        stdscr.addstr(0, 0, 'No entries found. Check your RSS feed URL.')
        stdscr.refresh()
        stdscr.getch()
        return

    favorites = []
    idx = 0
num_entries = len(entries)
    while True:
while True:
        stdscr.clear()
        header = "RSS Reader (Feedly-style shortcuts) - j/k: navigate, space: read, o: open externally, s or l: add to favorites, f: favorites, q: quit"
        stdscr.addstr(0, 0, header)

        # Get current window width
        height, width = stdscr.getmaxyx()
        
# Display entries using full window width in the format: date | source | title
        for i, entry in enumerate(entries):
            # Prepare strings
    date_str = time.strftime('%Y-%m-%d', entry.published_parsed) if hasattr(entry, 'published_parsed') else 'No Date'
    source = entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else 'Unknown'
    title = entry.title if hasattr(entry, 'title') else 'No Title'
    
    # Apply dim attribute if article has been read
    title_attr = 0
    if hasattr(entry, 'link') and entry.link in read_articles:
        title_attr = curses.A_DIM
    
    separator = " | "
    
    # Adjust title if total length exceeds window width
    height, width = stdscr.getmaxyx()
    total_len = len(date_str) + len(separator) + len(source) + len(separator) + len(title)
    if total_len > width - 1:
        # Truncate title to fit
        available = width - 1 - (len(date_str) + len(separator)*2 + len(source))
        title = title[:available]
    
    if i == idx:
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(i + 2, 0, date_str)
        stdscr.addstr(i + 2, len(date_str), separator)
        stdscr.addstr(i + 2, len(date_str) + len(separator), source, curses.A_REVERSE | curses.color_pair(1))
        stdscr.addstr(i + 2, len(date_str) + len(separator) + len(source), separator, curses.A_REVERSE)
        stdscr.addstr(i + 2, len(date_str) + 2*len(separator) + len(source), title, curses.A_REVERSE | title_attr)
        stdscr.attroff(curses.A_REVERSE)
    else:
        stdscr.addstr(i + 2, 0, date_str)
        stdscr.addstr(i + 2, len(date_str), separator)
        stdscr.addstr(i + 2, len(date_str) + len(separator), source, curses.color_pair(1))
        stdscr.addstr(i + 2, len(date_str) + len(separator) + len(source), separator)
        stdscr.addstr(i + 2, len(date_str) + 2*len(separator) + len(source), title, title_attr)
            source = entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else 'Unknown'
            title = entry.title if hasattr(entry, 'title') else 'No Title'
            
            # Apply dim attribute if article has been read
            title_attr = 0
            if hasattr(entry, 'link') and entry.link in read_articles:
                title_attr = curses.A_DIM
            
            separator = " | "
            
            # Adjust title if total length exceeds window width
            height, width = stdscr.getmaxyx()
            total_len = len(date_str) + len(separator) + len(source) + len(separator) + len(title)
            if total_len > width - 1:
                # Truncate title to fit
                available = width - 1 - (len(date_str) + len(separator)*2 + len(source))
                title = title[:available]
            
if i == idx:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(i + 2, 0, date_str)
                stdscr.addstr(i + 2, len(date_str), separator)
                stdscr.addstr(i + 2, len(date_str) + len(separator), source, curses.A_REVERSE | curses.color_pair(1))
                stdscr.addstr(i + 2, len(date_str) + len(separator) + len(source), separator, curses.A_REVERSE)
                stdscr.addstr(i + 2, len(date_str) + 2*len(separator) + len(source), title, curses.A_REVERSE | title_attr)
                stdscr.attroff(curses.A_REVERSE)
else:
                stdscr.addstr(i + 2, 0, date_str)
                stdscr.addstr(i + 2, len(date_str), separator)
                stdscr.addstr(i + 2, len(date_str) + len(separator), source, curses.color_pair(1))
                stdscr.addstr(i + 2, len(date_str) + len(separator) + len(source), separator)
                stdscr.addstr(i + 2, len(date_str) + 2*len(separator) + len(source), title, title_attr)

        stdscr.refresh()

        key = stdscr.getch()
        if key in [ord('q')]:
            break
        elif key in [ord('j')]:
            if idx < num_entries - 1:
                idx += 1
        elif key in [ord('k')]:
            if idx > 0:
                idx -= 1
elif key in [ord(' ')]:
            # Read the currently selected article within Warp
            read_article(stdscr, entries[idx])
            # Mark as read if link is available
            if hasattr(entries[idx], 'link'):
                read_articles.add(entries[idx].link)
        elif key in [ord('o')]:
            # Open the currently selected article in the default web browser
            if hasattr(entries[idx], 'link'):
                webbrowser.open(entries[idx].link)
        elif key in [ord('s'), ord('l')]:
            # Add the currently selected article to favorites if not already added
            if entries[idx] not in favorites:
                favorites.append(entries[idx])
                # Temporary feedback message
                stdscr.addstr(num_entries + 3, 0, 'Article added to favorites!')
                stdscr.refresh()
                curses.napms(1000)
elif key in [ord('f')]:
            # Enter favorites mode
            favorites_mode(stdscr, favorites)
        
        save_favorites(favorites)


def save_favorites(favorites):
    """Save favorites to a file for later reading."""
    try:
        with open("favorites.txt", "w") as f:
            for i, entry in enumerate(favorites):
                title = entry.title if hasattr(entry, 'title') else 'No Title'
                link = entry.link if hasattr(entry, 'link') else 'No Link'
                f.write(f"{i+1}. {title} - {link}\n")
    except Exception as e:
        pass


def favorites_mode(stdscr, favorites):
    """Display the list of favorite articles in the same format as the main list and allow opening an article by number."""
    stdscr.clear()
stdscr.addstr(0, 0, f"FAVORITES | {len(favorites)}")
    height, width = stdscr.getmaxyx()
    separator = " | "
    for i, entry in enumerate(favorites):
        date_str = time.strftime('%Y-%m-%d', entry.published_parsed) if hasattr(entry, 'published_parsed') else 'No Date'
        source = entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else 'Unknown'
        title = entry.title if hasattr(entry, 'title') else 'No Title'
        total_len = len(date_str) + len(separator) + len(source) + len(separator) + len(title)
        if total_len > width - 1:
            available = width - 1 - (len(date_str) + len(separator)*2 + len(source))
            title = title[:available]
        stdscr.addstr(i + 2, 0, date_str)
        stdscr.addstr(i + 2, len(date_str), separator)
        stdscr.addstr(i + 2, len(date_str) + len(separator), source, curses.color_pair(1))
        stdscr.addstr(i + 2, len(date_str) + len(separator) + len(source), separator)
        stdscr.addstr(i + 2, len(date_str) + 2*len(separator) + len(source), title)
    stdscr.refresh()
    # Navigation within favorites using j/k
    fav_idx = 0
    num_favs = len(favorites)
    while True:
        key = stdscr.getch()
        if key in [ord('q')]:
            break
        elif key in [ord('j')]:
            if fav_idx < num_favs - 1:
                fav_idx += 1
        elif key in [ord('k')]:
            if fav_idx > 0:
                fav_idx -= 1
        elif key in [ord(' ')]:
            read_article(stdscr, favorites[fav_idx])
            if hasattr(favorites[fav_idx], 'link'):
                read_articles.add(favorites[fav_idx].link)
        elif key in [ord('o')]:
            if hasattr(favorites[fav_idx], 'link'):
                webbrowser.open(favorites[fav_idx].link)
        # Update favorites display highlighting current selection
        for i, entry in enumerate(favorites):
            date_str = time.strftime('%Y-%m-%d', entry.published_parsed) if hasattr(entry, 'published_parsed') else 'No Date'
            source = entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else 'Unknown'
            title = entry.title if hasattr(entry, 'title') else 'No Title'
            total_len = len(date_str) + len(separator) + len(source) + len(separator) + len(title)
            if total_len > width - 1:
                available = width - 1 - (len(date_str) + len(separator)*2 + len(source))
                title = title[:available]
            if i == fav_idx:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(i + 2, 0, date_str)
                stdscr.addstr(i + 2, len(date_str), separator)
                stdscr.addstr(i + 2, len(date_str) + len(separator), source, curses.A_REVERSE | curses.color_pair(1))
                stdscr.addstr(i + 2, len(date_str) + len(separator) + len(source), separator, curses.A_REVERSE)
                stdscr.addstr(i + 2, len(date_str) + 2*len(separator) + len(source), title, curses.A_REVERSE)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, date_str)
                stdscr.addstr(i + 2, len(date_str), separator)
                stdscr.addstr(i + 2, len(date_str) + len(separator), source, curses.color_pair(1))
                stdscr.addstr(i + 2, len(date_str) + len(separator) + len(source), separator)
                stdscr.addstr(i + 2, len(date_str) + 2*len(separator) + len(source), title)
        stdscr.refresh()
    stdscr.clear()
    stdscr.refresh()

def read_article(stdscr, entry):
    """Display the selected article details: title, published date, and content, within Warp."""
    stdscr.clear()
    # Display title
    title = entry.title if hasattr(entry, 'title') else 'No Title'
    stdscr.addstr(0, 0, "Title: " + title)
    
    # Display published date
    if hasattr(entry, 'published'):
        date = entry.published
    elif hasattr(entry, 'updated'):
        date = entry.updated
    else:
        date = "No Date"
    stdscr.addstr(1, 0, "Date: " + date)
    
    # Display content or summary
    if hasattr(entry, 'content'):
        content = entry.content[0].value
    elif hasattr(entry, 'summary'):
        content = entry.summary
    else:
        content = "No Content Available"

    # Use the full window width to wrap the content
    import textwrap
    height, width = stdscr.getmaxyx()
    wrapped_lines = textwrap.wrap(content, width=width - 1)
    row = 3
    for line in wrapped_lines:
        # Truncate the line if it's too long, though textwrap should handle it
        if len(line) > width - 1:
            line = line[:width - 1]
        stdscr.addstr(row, 0, line)
        row += 1
        if row >= height - 1:
            break

    stdscr.addstr(curses.LINES-1, 0, "Press any key to return")
    stdscr.refresh()
    stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)

