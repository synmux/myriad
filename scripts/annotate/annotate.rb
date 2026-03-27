#!/usr/bin/env ruby
# frozen_string_literal: true

require 'open3'

KEY_ID = '065602DAF36C71E6AB3A8D7014E5DFDDDAF9DBBF' # your key ID

DOMAINS = %w[
  badreputation.org.uk
  basilisk.gallery
  basilisk.nexus
  basilisk.photos
  basilisk.video
  clarion.sh
  dcw.soy
  dmaf.uk
  genderbase.com
  paginator.app
  sl1p.dev
  sl1p.email
  sl1p.net
  sl1p.services
  sl1p.space
  sl1p.systems
  syn.as
  syn.haus
  syn.horse
  syn.ing
  syn.pink
].freeze # chuck all 23 in here

DOMAINS.each_with_index do |domain, i|
  notation = "proof@ariadne.id=dns:#{domain}?type=TXT"

  commands = "notation\n#{notation}\nsave\n"

  _stdout, stderr, status = Open3.capture3(
    'gpg', '--command-fd', '0',
    '--status-fd', '2',
    '--no-tty',
    '--edit-key', KEY_ID,
    stdin_data: commands
  )

  if status.success?
    puts "[#{i + 1}/#{DOMAINS.length}] ✓ #{domain}"
  else
    warn "[#{i + 1}/#{DOMAINS.length}] ✗ #{domain}"
    warn stderr
  end
end

puts "\nDone. Verify with:"
puts "  gpg --list-options show-notations --list-sigs #{KEY_ID}"
