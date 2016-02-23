require 'webrick'
require 'webrick/https'
include WEBrick

#root = File.expand_path './public'



server = HTTPServer.new(
  :BindAddress => 'spike.asu.edu',
  :Port => '5051',
  #:DocumentRoot => root,
  :SSLEnable => true,
  
)

# Shutdown gracefully on signal interrupt CTRL-C
# http://www.ruby-doc.org/core-2.1.1/Kernel.html#method-i-trap
trap('INT') { server.shutdown }

server.start
