from usp.tree import sitemap_tree_for_homepage
from termcolor import colored
import sys
import threading, os
from tld import get_tld


def url_to_domain(url):
    res = get_tld(url, as_object=True)
    return res.fld.replace('.', '_')


def run_sitemap(url_web):
    tree = sitemap_tree_for_homepage(url_web)

    # all_pages() returns an Iterator
    sitemaps = []

    data = tree.sub_sitemaps

    urls_sitemaps = []
    for item in data:
        sub_sitemaps = item.sub_sitemaps
        if type(item).__name__ != 'IndexRobotsTxtSitemap':
            urls_sitemaps.append(item.url)
        for sitemap in sub_sitemaps:
            if hasattr(sitemap, 'sub_sitemaps') and sitemap.sub_sitemaps:
                for data in sitemap.sub_sitemaps:
                    urls_sitemaps.append(data.url)
            urls_sitemaps.append(sitemap.url)

    with open(f"datas/list_sitemap_{url_to_domain(url_web)}.txt", "w") as list_sitemap:
        list_sitemap.write("\n".join(urls_sitemaps))

    urls = {page.url for page in tree.all_pages()}
    urls = list(urls)

    with open(f"datas/list_urls_{url_to_domain(url_web)}.txt", "w") as list_urls:
        list_urls.write("\n".join(urls))


th = []
with open("urls.txt") as urls_website:
    for url_web in urls_website:
        thread = threading.Thread(target=run_sitemap, args=(url_web,))
        th.append(thread)
        thread.start()

for t in th:
    t.join()

print(colored('Liste de sitemap créé avec succés', 'green'))
print(colored('Liste des urls de tous les sitemaps créé avec succés', 'green'))
