

import os, time
from markdown import markdown
# HTML Cleaning
from bs4 import BeautifulSoup

# Make sure we're in the right directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def files_in_directory(directory):
  return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def read_root(root_name):
  with open(os.path.join("roots", root_name), 'r') as f:
    return f.read()

def read_branch(branch_name):
  with open(os.path.join("branches", branch_name), 'r') as f:
    return f.read()

def build_page(filename, title, navbar, content, year):
  output = str(template)
  output = output.replace("{title}", title)
  output = output.replace("{navbar}", navbar)
  output = output.replace("{content}", content)
  output = output.replace("{year}", str(year))
  # Convert output to HTML
  output = markdown(output)
  # Clean HTML
  output = BeautifulSoup(output, "html.parser").prettify()
  with open(filename, "w+") as f:
    f.write(output)

def fill_links(content, link_list):
  for link in link_list:
    content = content.replace(link[0], link[1])
  return content


## Get list of roots and branches and load the template ##
root_list = files_in_directory("roots")
branch_list = files_in_directory("branches")
with open('template.txt', 'r') as f:
  template = f.read()


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
root_list = new_root_list


## Build the navbar ##
navbar_list = []
for page in root_list:
  title = page.split('.')[0]
  if title == "Home":
    navbar_list.append("[Home](/index)")
  else:
    navbar_list.append("[{}](/{})".format(title, title))
navbar = " - ".join(navbar_list)


## Generate link list
link_list = []
for page in root_list:
  title = page.split(".")[0]
  if title == "Home":
    # Fix the Home link
    link_list.append(["Home", "[Home](/index)"])
  else:
    link_list.append([title, "[{}](/{})".format(title, title)])
for page in branch_list:
  title = page.split(".")[0]
  link_list.append([title, "[{}](/{})".format(title, title)])



## Delete old pages ##
for old_file in os.listdir('.'):
  if os.path.isfile(old_file) and old_file.split('.')[1] == "html":
    os.remove(old_file)


## Build the pages ##
year = time.strftime("%Y")
for page in root_list:
  title = page.split(".")[0]
  if title == "Home":
    filename = "index.html"
  else:
    filename = "{}.html".format(title)
  content = read_root(page)
  content = fill_links(content, link_list)
  build_page(filename, title, navbar, content, year)
for page in branch_list:
  title = page.split(".")[0]
  content = read_branch(page)
  content = fill_links(content, link_list)
  build_page("{}.html".format(title), title, navbar, content, year)


