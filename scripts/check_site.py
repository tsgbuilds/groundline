"""Validate the static site's crawl paths and page metadata without dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / 'dist'
ORIGIN = 'https://ground-line-tree-stump.sunset-tune-1548.chatgpt.site'

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.canonicals, self.descriptions = [], [], [], []
        self.titles, self.schemas, self.h1 = [], [], 0
        self.active = None
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.active = ['title', '']
        if tag == 'script' and attrs.get('type') == 'application/ld+json': self.active = ['schema', '']
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonicals.append(attrs['href'])
        if tag == 'meta' and attrs.get('name') == 'description': self.descriptions.append(attrs['content'])
        for key in ('href', 'src'):
            if key in attrs: self.refs.append(attrs[key])
    def handle_data(self, data):
        if self.active is not None: self.active[1] += data
    def handle_endtag(self, tag):
        if self.active and ((tag == 'title' and self.active[0] == 'title') or (tag == 'script' and self.active[0] == 'schema')):
            if self.active[0] == 'title': self.titles.append(self.active[1])
            else: self.schemas.append(json.loads(self.active[1]))
            self.active = None

pages = {path: Page(path.read_text()) for path in ROOT.rglob('*.html')}
assert len(pages) == 5, f'Expected homepage, three service pages, and service-area directory, got {len(pages)}'
canonicals, titles, descriptions = set(), set(), set()
for path, page in pages.items():
    relative = path.relative_to(ROOT).as_posix()
    route = '/' + relative.removesuffix('index.html')
    assert len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {path}'
    assert page.h1 == 1 and len(page.titles) == 1, f'Heading/title error: {path}'
    assert page.canonicals == [ORIGIN + route], f'Canonical error: {path}'
    assert len(page.descriptions) == 1 and page.descriptions[0], f'Description error: {path}'
    assert page.schemas and all(s.get('@context') == 'https://schema.org' for s in page.schemas)
    assert 'Ground Line' in path.read_text() and '(832) 501-9594' in path.read_text()
    assert not any(name in path.read_text().lower() for name in ('erik', 'shrout', 'ejs2013'))
    canonicals.update(page.canonicals); titles.update(page.titles); descriptions.update(page.descriptions)
    for ref in page.refs:
        u = urlsplit(ref)
        if u.scheme == 'tel': assert u.path == '+18325019594'
        if u.scheme == 'sms': assert u.path == '+18325019594'
        if u.scheme and (u.scheme not in ('http', 'https') or u.netloc != urlsplit(ORIGIN).netloc): continue
        if u.netloc and u.netloc != urlsplit(ORIGIN).netloc: continue
        target = ROOT / unquote(u.path).lstrip('/') if u.path.startswith('/') else path.parent / unquote(u.path)
        if not u.path: target = path
        if target.is_dir(): target = target / 'index.html'
        assert target.exists(), f'Broken link on {relative}: {ref}'
        if u.fragment and target in pages: assert u.fragment in pages[target].ids, f'Broken fragment: {ref}'
    print(f'PASS {route}')
assert len(titles) == len(pages) and len(descriptions) == len(pages), 'Duplicate page metadata'
sitemap = ET.parse(ROOT / 'sitemap.xml')
locations = {e.text for e in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
assert locations == canonicals, 'Sitemap and canonical URLs differ'
robots = (ROOT / 'robots.txt').read_text()
assert 'Allow: /' in robots and f'Sitemap: {ORIGIN}/sitemap.xml' in robots
print('PASS internal links, assets, phone, metadata, schemas, sitemap, and public-copy name check')
