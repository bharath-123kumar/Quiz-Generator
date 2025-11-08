import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

USER_AGENT = "Mozilla/5.0 (compatible; WikiQuizBot/1.0)"

def fetch_html(url, timeout=12):
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.text

def parse_wikipedia(html):
    soup = BeautifulSoup(html, "html.parser")
    # Title
    title = soup.find(id="firstHeading").get_text(strip=True) if soup.find(id="firstHeading") else soup.title.string
    # First paragraphs for summary
    content_div = soup.find("div", {"class": "mw-parser-output"})
    summary = ""
    sections = []
    full_text = []
    if content_div:
        # collect leading paragraphs
        for p in content_div.find_all("p", recursive=False):
            txt = p.get_text(strip=True)
            if txt:
                summary += txt + "\n\n"
                full_text.append(txt)
                # break after a few paras? keep a couple
                if len(summary.split()) > 200:
                    break
        # sections: h2 headings with their paragraph text
        for header in content_div.find_all(["h2","h3"]):
            heading_text = header.get_text(strip=True).replace("[edit]","").strip()
            # collect following sibling paragraphs until next header
            sec_text = ""
            for sib in header.next_siblings:
                if sib.name and sib.name.startswith('h'):
                    break
                if sib.name == "p":
                    sec_text += sib.get_text(strip=True) + "\n"
            if heading_text and sec_text:
                sections.append({"heading": heading_text, "text": sec_text})
                full_text.append(heading_text + ": " + sec_text)
    scraped_text = "\n\n".join(full_text)
    return {
        "title": title,
        "summary": summary.strip(),
        "sections": sections,
        "scraped_text": scraped_text
    }

# very simple entity finder (placeholder — replace with spaCy for production)
def extract_entities(text):
    people = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b', text)[:20]
    # naive dedupe
    def uniq(lst):
        seen, out = set(), []
        for x in lst:
            if x not in seen:
                out.append(x); seen.add(x)
        return out
    return {
        "people": uniq(people)[:10],
        "organizations": [],
        "locations": []
    }
