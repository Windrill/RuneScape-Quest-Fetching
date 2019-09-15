from html.parser import HTMLParser

# RS Parser collects html elements
class rsParser(HTMLParser):
  # HTML Self Closing Tags
  self_closing = ["area", "base", "br", "col", "embed", "hr", "img", "input", "keygen", "link", "menuitem", "meta", "param", "source", "track", "wbr"]
  # https://runescape.fandom.com
  base_url = "runescape.fandom.com"
  def __init__(self):
    super().__init__()
    self.parents = []
    
  def handle_starttag(self, tag, attrs):
    if tag not in rsParser.self_closing:
      self.parents.append(tag)

      