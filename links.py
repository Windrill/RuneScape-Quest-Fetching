from cparser import rsParser

# Link Parser collects links to quests
class linkParser(rsParser):
  combination = ["li", "div", "noscript"]
  def __init__(self):
    super().__init__()
    self.links = []
  
  def divFollowsLi(self):
    for i in range(len(self.parents)):
      if i>0 and self.parents[i] == "div" and self.parents[i-1] == "li":
        return True
    return False
    
  def handle_starttag(self, tag, attrs):
    super().handle_starttag(tag,attrs)
    for (name, data) in attrs:
      if name == "href" and self.parents and tag != "link":
        if all([c in self.parents for c in linkParser.combination]) and self.divFollowsLi():
          if rsParser.base_url in data:
            self.links.append(data)
          else: 
            self.links.append(rsParser.base_url + data)
            
  # The tags don't cancel each other in this situation; in this occasion, the last 'few' historical tags 
  # were used to identify the type of the text
  def handle_endtag(self, tag):
    if tag not in rsParser.self_closing:
      self.parents = self.parents[1:]
      