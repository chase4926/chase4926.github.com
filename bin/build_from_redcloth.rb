
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


file_paths = search_directory('../redcloth', '*.txt')
file_paths.each do |path|
  redcloth_html = ''
  File.open(path, 'r') do |file|
    redcloth_html = RedCloth.new(file.read).to_html
  end
  File.open("../#{path.split('/').last.split('.txt')[0]}.html",'w+') do |file|
    file.print redcloth_html
  end
end
