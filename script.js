/* Script for monarch project: Implements Feedly-style shortcuts for navigating news articles */

document.addEventListener('DOMContentLoaded', function() {
    const articles = document.querySelectorAll('.news-item');
    let activeIndex = 0;

    // Helper function to update active state
    function updateActiveArticle(index) {
        articles.forEach((article, i) => {
            if (i === index) {
                article.classList.add('active');
                article.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                article.classList.remove('active');
            }
        });
    }

    // Set the first article as active on page load
    if (articles.length > 0) {
        updateActiveArticle(activeIndex);
    }

    document.addEventListener('keydown', function(event) {
        // Prevent key events when focused on input or textarea
        const tag = document.activeElement.tagName.toLowerCase();
        if (tag === 'input' || tag === 'textarea') {
            return;
        }

        switch (event.key.toLowerCase()) {
            case 'j':
                // Navigate to next article
                if (activeIndex < articles.length - 1) {
                    activeIndex++;
                    updateActiveArticle(activeIndex);
                }
                break;
            case 'k':
                // Navigate to previous article
                if (activeIndex > 0) {
                    activeIndex--;
                    updateActiveArticle(activeIndex);
                }
                break;
            case 'o':
                // Open active article's link if available
                const link = articles[activeIndex].querySelector('a');
                if (link && link.href) {
                    window.open(link.href, '_blank');
                }
                break;
            default:
                break;
        }
    });
});

