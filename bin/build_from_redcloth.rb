
require 'rubygems'
require 'RedCloth'

def search_directory(folder='.', search_for='*')
  result = []
  if search_for != nil then
    search_for = File.join(folder, search_for)
  else
    search_for = folder
  end
  Dir.glob(search_for).each do |file|
    result << file
  end
  return result
end


header = ''
File.open('../redcloth/header.template','r') do |file|
  header = file.read
end
footer = ''
File.open('../redcloth/footer.template','r') do |file|
  footer = file.read
end


file_paths = search_directory('../redcloth', '*.txt')
file_paths.each do |path|
  content = ''
  File.open(path, 'r') do |file|
    content = file.read
  end
wrapper =<<END
#{header}
#{content}
#{footer}
END
  redcloth_html = RedCloth.new(wrapper).to_html
  File.open("../#{path.split('/').last.split('.txt')[0]}.html",'w+') do |file|
    file.print redcloth_html
  end
end
