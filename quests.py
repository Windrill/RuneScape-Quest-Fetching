from cparser import rsParser

# Collects information about a quest
class questParser(rsParser):
  def __init__(self):
    super().__init__()
    self.title = ""
    # Switches to collect data: Title, Quest, Characters (<a>) in the quest
    self.titleCount = False
    self.questStart = False
    self.linkCancel = False
    # A Subsection's Font Size (Eg: A chapter such as "King Veldaban's Dilemma", 2 for <h2>)
    self.headers = 0
    # Additional Section Switches: Prompts on top and table on bottom
    self.ignore = False
    self.infoTable = False
    
    # docx writing and setting up
    self.document = Document()
    cstyle = self.document.styles['Normal']
    cstyle.paragraph_format.space_before = Pt(0)
    cstyle.paragraph_format.space_after = Pt(1)
    cstyle.font.name = 'Heveltica'
    
  def handle_starttag(self, tag, attrs):
    if tag == "h1" and ("class", "page-header__title") in attrs:
      self.titleCount = True
    # Quest Start: 
    elif tag == "div":
      for (name, data) in attrs:
        if (name == "id" and data == "mw-content-text") or (name == "class" and "mw-content-text" in data):
          self.questStart = True
          break
    # Tables: Prompts on top & info on bottom
    elif self.questStart and tag == "table":
      for (name, data) in attrs:
        if name == "class" and "messagebox" in data:
          self.ignore = True
          self.ignoreConctent = tag
          break
        # Table with links to related items transformed into text
        elif name == "class" and "nowraplinks" in data:
          self.infoTable = True
          self.lastp = self.document.add_paragraph("")
    # Subsection Headers
    elif self.questStart and tag[0] == "h":
      print(tag, attrs)
      self.headers = int(tag[1])
      
    # Record quest information if quest starts      
    if self.questStart:
      super().handle_starttag(tag,attrs)

  def handle_data(self, data):
    processed_data = (data.replace("\n", "")).encode(cencode, 'ignore').decode(cencode)
    
    # Title
    if self.titleCount:
      self.title = processed_data
      self.document.add_heading(self.title, 0).bold = True
      self.titleCount = False
      
    # Quest Body
    elif self.questStart and processed_data.strip() != "":
      recent = self.parents[-1]
      # Message Prompt: Ignore
      if self.ignore:
        pass
      elif self.infoTable:
        # Remove three valueless characters in the table on the bottom
        if len(data) <= 1:
          return
        # Content below can be formulated into a table
        # [Similar to] Column in the table
        if recent == "a":
          self.lastp.add_run(processed_data + ", ")
        # [Similar to] New row in the table
        else:
          self.lastp = self.document.add_paragraph(processed_data + ": ")
          
      # <a> The HTML element after <a> is inline instead of a paragraph like <p>
      elif self.linkCancel:
        self.lastp.add_run(processed_data)
        self.linkCancel = False
        
      # Section Header
      elif self.headers != 0 and recent == "span":
        head = self.parents[-1]
        print("hmm", type(self.headers), self.headers)
        self.document.add_heading(processed_data, level=self.headers)
        self.headers = 0
        
      # Bold, Italics, Inline links
      elif recent not in ["b", "i", "a"]:
        self.lastp = self.document.add_paragraph(processed_data)
        
      elif recent == "b":
        self.lastp = self.document.add_paragraph()
        self.lastp.add_run(processed_data).bold = True
        
      elif recent == "i":
        self.lastp = self.document.add_paragraph()
        self.lastp.add_run(processed_data).italic = True
        
      # Links are inline and must not be counted as a new paragraph, as well as the element after that
      elif recent == "a":
        self.lastp.add_run(processed_data)
        self.linkCancel = True
      # Contains a new paragraph
      else:
        self.lastp.add_run(processed_data)
        
      # Logging:
      print(self.parents, processed_data)
      
  def handle_endtag(self, tag):
    if not self.questStart or (tag in rsParser.self_closing):
      return
    # Ignore message: Match <table> and ignore condition
    if self.ignore and self.ignoreConctent == tag:
      self.ignore = False
      
    # HTML tags are like a stack except for tables
    #if self.parents[-1] != tag:
    #  print("open-tag does not match end-tag:", self.parents[-1], tag)
    self.parents = self.parents[:-1]
    
    if len(self.parents) == 0:
      # print("End quest section")
      self.questStart = False
      try:
        os.remove(self.title+".docx")
      except OSError:
        pass
      validTitle = re.sub("[^a-zA-Z_'!() ]", "", self.title)
      self.document.save("./quests/" + validTitle + ".docx")
    # Subsection Font Size Reset
    if tag[0] == "h":
      self.headers = 0
