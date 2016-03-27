

import os, re, time
from markdown import markdown
# HTML Cleaning
from bs4 import BeautifulSoup

# Make sure we're in the right directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def files_in_directory(directory):
  return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def replace_at_index(string, index, pattern, replacement):
  return string[:index] + string[index:].replace(pattern, replacement, 1)


class SiteBuilder:
  def __init__(self):
    ## Get list of roots and branches and load the template ##
    root_list = files_in_directory("roots")
    self.branch_list = files_in_directory("branches")
    with open('template.txt', 'r') as f:
      self.template = f.read()
    ## Rebuild root_list to match order.txt ##
    with open('order.txt', 'r') as f:
      order = f.read()
    order = order.splitlines()[0].split(',')
    # Find the wildcard index
    wild_index = order.index("*")
    # Make a list of items sorted before and after the wildcard
    before_list = order[:wild_index]
    after_list = order[wild_index+1:]
    # Find the number of items in the wildcard
    other_number = len(root_list)-(len(before_list)+len(after_list))
    new_root_list = root_list[:]
    for item in before_list:
      if item in root_list:
        root_list.remove(item)
        new_root_list[before_list.index(item)] = item
    for item in after_list:
      if item in root_list:
        root_list.remove(item)
        new_root_list[after_list.index(item)+wild_index+other_number] = item
    for index, item in enumerate(root_list):
      new_root_list[wild_index+index] = item
    self.root_list = new_root_list
    ## Build Navbar and generate link_list ##
    self.build_navbar()
    self.generate_link_keywords()
    ## Add regex patterns to blacklist areas where auto-linking isn't allowed
    self.blacklisted_patterns = ['#([^#]+)#', # Prevents links # here #
                                 '\(([^\(\)]+)\)', # Prevents links ( here )
                                 '\[([^\[\]]+)\]'] # Prevents links [ here ]

  def read_root(self, root_name):
    with open(os.path.join("roots", root_name), 'r') as f:
      return f.read()

  def read_branch(self, branch_name):
    with open(os.path.join("branches", branch_name), 'r') as f:
      return f.read()

  def get_match_index(self, match, string):
    # Returns the index of a string in a match
    if string in match.group(0):
      index = match.start()
      index += match.group(0).index(string)
      return index
    else:
      return False

  def get_bad_indices(self, content):
    # bad indices >> indices that aren't allowed to be auto-linked
    index_list = []
    for regex in self.blacklisted_patterns:
      for match in re.finditer(regex, content):
        for link in self.link_keywords:
          #print(content[get_match_index(match, link)])
          index = self.get_match_index(match, link)
          if index:
            index_list.append(index)
    return index_list

  def build_page(self, filename, title, content, year):
    output = str(self.template)
    output = output.replace("{title}", title)
    # Convert navbar to HTML
    output = output.replace("{navbar}", markdown(self.navbar))
    # Convert content to HTML
    output = output.replace("{content}", markdown(content))
    output = output.replace("{year}", str(year))
    # Clean HTML
    output = BeautifulSoup(output, "html.parser").prettify()
    with open(filename, "w+") as f:
      f.write(output)

  def fill_links(self, content):
    ## Generate Bad Indices ##
    bad_index_list = self.get_bad_indices(content)
    ## Generate Replacables and indices ##
    replacable_list = []
    for link in self.link_keywords:
      replacable_list += [[match.start(), link] for match in re.finditer(re.escape(link), content)]
    ## Remove items from replacable_list that are on bad_index_list
    to_remove = [index for index, value in enumerate(replacable_list) if value[0] in bad_index_list]
    for index in reversed(to_remove):
      del replacable_list[index]
    ## Make the substitutions in reverse order ##
    for index, pattern in reversed(replacable_list):
      content = replace_at_index(content, index, pattern, self.get_keyword_replacement(pattern))
    return content

  def build_navbar(self):
    navbar_list = []
    for page in self.root_list:
      title = page.split('.')[0]
      if title == "Home":
        navbar_list.append("[Home](/index)")
      else:
        navbar_list.append("[{}](/{})".format(title, title))
    self.navbar = " - ".join(navbar_list)

  def generate_link_keywords(self):
    ## Generate link list
    self.link_keywords = []
    for page in self.root_list:
      title = page.split(".")[0]
      self.link_keywords.append(title)
    for page in self.branch_list:
      title = page.split(".")[0]
      self.link_keywords.append(title)

  def get_keyword_replacement(self, keyword):
    if keyword == "Home":
      return "[Home](/index)"
    else:
      return "[{}](/{})".format(keyword, keyword)

  def build(self):
    ## Delete old pages ##
    for old_file in os.listdir('.'):
      if os.path.isfile(old_file) and old_file.split('.')[1] == "html":
        os.remove(old_file)

    ## Build the pages ##
    year = time.strftime("%Y")
    for page in self.root_list:
      title = page.split(".")[0]
      if title == "Home":
        filename = "index.html"
      else:
        filename = "{}.html".format(title)
      content = self.read_root(page)
      content = self.fill_links(content)
      self.build_page(filename, title, content, year)
    for page in self.branch_list:
      title = page.split(".")[0]
      content = self.read_branch(page)
      content = self.fill_links(content)
      self.build_page("{}.html".format(title), title, content, year)


site = SiteBuilder()
site.build()

