import re

with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'r') as f:
    content = f.read()

# Fix paths for archive
content = content.replace('images/', '../../../images/')
content = content.replace('videos/', '../../../videos/')
content = content.replace('href="index.html"', 'href="../../../index.html"')
content = content.replace('href="history.html"', 'href="../../../history.html"')
content = content.replace('href="about.html"', 'href="../../../about.html"')
content = content.replace('href="contact.html"', 'href="../../../contact.html"')
content = content.replace('href="rss.xml"', 'href="../../../rss.xml"')

with open('/home/swg/.openclaw/workspace/news-blog/history/2026/07/20260711.html', 'w') as f:
    f.write(content)

print("Archive created: history/2026/07/20260711.html")