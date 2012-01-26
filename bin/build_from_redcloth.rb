
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

def wrap_it_up(title, header, content, footer)
return <<END
<html>
#{title}
#{header}
#{content}
#{footer}
</html>
END
end

def read_file(path)
  File.open(path,'r') do |file|
    return file.read
  end
end


file_paths = search_directory('../redcloth', '*.txt')
file_paths.each do |path|
  title, content = read_file(path).split("\n", 2)
  wrapper = wrap_it_up(title,
                       read_file('../redcloth/header.template'),
                       content,
                       read_file('../redcloth/footer.template'))
  redcloth_html = RedCloth.new(wrapper).to_html
  redcloth_html.gsub!("\t",'  ')
  File.open("../#{path.split('/').last.split('.txt')[0]}.html",'w+') do |file|
    file.print redcloth_html
  end
end
