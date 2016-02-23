require 'webrick'
include WEBrick

#root = File.expand_path './public'

cert_name = [
  %w[CN localhost],
]

server = HTTPServer.new(
  :BindAddress => 'spike.asu.edu',
  :Port => '5000',
 # :DocumentRoot => root,
  :SSLEnable => true,
  :SSLCertName => cert_name # LOOK! SSLCertName IS SET!
)

# Shutdown gracefully on signal interrupt CTRL-C
# http://www.ruby-doc.org/core-2.1.1/Kernel.html#method-i-trap
trap('INT') { server.shutdown }

server.start
