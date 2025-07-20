# 2025-05-04 21:45:38 by RouterOS 7.19rc1
# software id = KH3M-8RQA
#
# model = RB5009UPr+S+
# serial number = HE108J2C6WG
/interface bridge
add add-dhcp-option82=yes \
    dhcp-snooping=yes igmp-snooping=yes name=br-private port-cost-mode=short
/interface ethernet
set [ find default-name=ether1 ] name=external
set [ find default-name=sfp-sfpplus1 ] disabled=yes name=sfp
/interface list
add name=iflist-wan
add name=iflist-lan
add name=iflist-cpe
add name=iflist-vpn
add name=iflist-auto-lan
add name=iflist-auto-wan
add name=iflist-auto-internet
add include=iflist-lan,iflist-vpn name=iflist-admin
add include=iflist-cpe,iflist-wan name=iflist-masquerade
/ip pool
add name=poolv4-br-private-dhcp ranges=10.0.101.100-10.0.101.199
/ip smb users
set [ find default=yes ] disabled=yes
/interface bridge port
add bridge=br-private interface=ether2
add bridge=br-private interface=ether3
add bridge=br-private interface=ether4
add bridge=br-private interface=ether5
add bridge=br-private interface=ether6
add bridge=br-private interface=ether7
add bridge=br-private interface=ether8
add bridge=br-private interface=ether9
add bridge=br-private interface=ether10
/interface bridge settings
set use-ip-firewall=yes use-ip-firewall-for-pppoe=yes \
    use-ip-firewall-for-vlan=yes
/ip firewall connection tracking
set udp-timeout=10s
/ip neighbor discovery-settings
set discover-interface-list=all
/ip settings
set tcp-syncookies=yes
/interface detect-internet
set detect-interface-list=all internet-interface-list=iflist-auto-internet \
    lan-interface-list=iflist-auto-lan wan-interface-list=iflist-auto-wan
/interface list member
add interface=br-private list=iflist-lan
add list=iflist-wan interface=external
add list=iflist-lan interface=ether2
add list=iflist-lan interface=ether3
add list=iflist-lan interface=ether4
add list=iflist-lan interface=ether5
add list=iflist-lan interface=ether6
add list=iflist-lan interface=ether7
add list=iflist-lan interface=ether8
add list=iflist-lan interface=ether9
add list=iflist-lan interface=ether10
add interface=external list=iflist-masquerade
/ip address
add address=10.0.101.1/24 interface=br-private network=10.0.101.0
/ip cloud
set ddns-enabled=yes ddns-update-interval=1h
/ip dhcp-client
add default-route-distance=10 interface=external use-peer-dns=no \
    use-peer-ntp=no
/ip dhcp-server network
add address=10.0.101.0/24 dns-server=10.0.101.1 gateway=10.0.101.1 netmask=24 \
    ntp-server=10.0.101.1
/ip dns
set allow-remote-requests=yes cache-max-ttl=5m cache-size=16384KiB \
    doh-max-concurrent-queries=5000 doh-max-server-connections=100 \
    max-concurrent-queries=100000 max-concurrent-tcp-sessions=100000 \
    query-server-timeout=5s query-total-timeout=20s use-doh-server=\
    https://dns.nextdns.io/ddf926 verify-doh-cert=yes
/ip dns static
add address=10.0.99.1 name=fw.parents.sl1p.net type=A
add address=108.61.173.154 name=dns.nextdns.io type=A
add address=45.142.244.191 name=dns.nextdns.io type=A
add address=2001:19f0:7400:137a:5400:4ff:fedf:6c6d name=dns.nextdns.io type=AAAA
add address=2a0f:3b03:100:2:5054:ff:fe90:4a77 name=dns.nextdns.io type=AAAA
/ip firewall address-list
add address=10.0.101.0/24 comment="internal br-private" list=list-v4-internal
add address=10.0.99.0/24 comment="parents rvnet" list=list-v4-trusted
add address=10.0.98.0/24 comment="parents sl1p" list=list-v4-trusted
/ip firewall filter
add action=accept chain=input
add action=accept chain=output
add action=accept chain=forward
add action=accept chain=input comment="accept internal to self" \
    src-address-list=list-v4-internal
add action=drop chain=input port=1080 protocol=tcp
add action=accept chain=input comment="accept ssh altport to self" dst-port=\
    212 protocol=tcp
add action=accept chain=input comment="accept winbox to self" dst-port=8291 \
    protocol=tcp
add action=accept chain=input comment="accept from trusted" src-address-list=\
    list-v4-trusted
add action=accept chain=input comment="accept established,related,untracked" \
    connection-state=established,related,untracked
add action=drop chain=input comment="drop invalid" connection-state=invalid
add action=accept chain=input comment="accept ICMP" protocol=icmp
add action=accept chain=input comment=\
    "accept to local loopback (for CAPsMAN)" dst-address=127.0.0.1
add action=drop chain=input comment="drop all not coming from admin ifs" \
    in-interface-list=!iflist-admin
add action=accept chain=forward comment="forward from trusted" \
    src-address-list=list-v4-trusted
add action=accept chain=forward comment="forward to trusted" \
    dst-address-list=list-v4-trusted
add action=accept chain=forward comment="accept in ipsec policy" \
    ipsec-policy=in,ipsec
add action=accept chain=forward comment="accept out ipsec policy" \
    ipsec-policy=out,ipsec
add action=fasttrack-connection chain=forward comment=fasttrack \
    connection-state=established,related disabled=yes hw-offload=yes
add action=accept chain=forward comment=\
    "accept established,related,untracked" connection-state=\
    established,related,untracked
add action=drop chain=forward comment="drop invalid" connection-state=invalid
add action=drop chain=forward comment="drop all from WAN not DSTNATed" \
    connection-nat-state=!dstnat connection-state=new in-interface-list=\
    iflist-wan
add action=accept chain=output comment="accept to trusted" dst-address-list=\
    list-v4-trusted
/ip firewall nat
add action=dst-nat chain=dstnat comment=plex@nas dst-port=32400 \
    in-interface-list=iflist-wan protocol=tcp to-addresses=10.0.98.11 \
    to-ports=32400
add action=dst-nat chain=dstnat comment=roon@nas dst-port=55000 \
    in-interface-list=iflist-wan protocol=tcp to-addresses=10.0.98.11 \
    to-ports=55000
add action=masquerade chain=srcnat comment=masquerade ipsec-policy=out,none \
    out-interface-list=iflist-wan
/ip firewall service-port
set irc disabled=no
set rtsp disabled=no
/ip ipsec profile
set [ find default=yes ] dpd-interval=2m dpd-maximum-failures=5
/ip proxy
set port=3128
/ip service
set ftp disabled=yes
set telnet disabled=yes
set www disabled=yes
set ssh port=212
set api disabled=yes
/ip ssh
set always-allow-password-login=yes forwarding-enabled=local host-key-size=\
    4096 strong-crypto=yes
/ip upnp
set enabled=yes
/ip upnp interfaces
add interface=external type=external
add interface=br-private type=internal
/ipv6 firewall address-list
add address=::/128 comment="unspecified address" list=list-v6-bogons
add address=::1/128 comment=lo list=list-v6-bogons
add address=fec0::/10 comment=site-local list=list-v6-bogons
add address=::ffff:0.0.0.0/96 comment=ipv4-mapped list=list-v6-bogons
add address=::/96 comment="ipv4 compat" list=list-v6-bogons
add address=100::/64 comment="discard only " list=list-v6-bogons
add address=2001:db8::/32 comment=documentation list=list-v6-bogons
add address=2001:10::/28 comment=ORCHID list=list-v6-bogons
add address=3ffe::/16 comment=6bone list=list-v6-bogons
add address=2001:8b0:65d3::/48 comment="7t54 aaisp full v6 allocation" list=\
    list-v6-trusted
/ipv6 firewall filter
add action=accept chain=input comment="accept from list-v6-trusted" \
    src-address-list=list-v6-trusted
add action=accept chain=input comment="accept established,related,untracked" \
    connection-state=established,related,untracked
add action=drop chain=input comment="drop invalid" connection-state=invalid
add action=accept chain=input comment="accept ICMPv6" protocol=icmpv6
add action=accept chain=input comment="accept UDP traceroute" port=\
    33434-33534 protocol=udp
add action=accept chain=input comment=\
    "accept DHCPv6-Client prefix delegation." dst-port=546 protocol=udp \
    src-address=fe80::/10
add action=accept chain=input comment="accept IKE" dst-port=500,4500 \
    protocol=udp
add action=accept chain=input comment="accept ipsec AH" protocol=ipsec-ah
add action=accept chain=input comment="accept ipsec ESP" protocol=ipsec-esp
add action=accept chain=input comment="accept all that matches ipsec policy" \
    ipsec-policy=in,ipsec
add action=drop chain=input comment=\
    "drop everything else not coming from LAN" in-interface-list=!iflist-lan
add action=accept chain=forward comment="forward from list-v6-trusted" \
    src-address-list=list-v6-trusted
add action=accept chain=forward comment="forward to list-v6-trusted" \
    dst-address-list=list-v6-trusted
add action=accept chain=forward comment=\
    "accept established,related,untracked" connection-state=\
    established,related,untracked
add action=drop chain=forward comment="drop invalid" connection-state=invalid
add action=drop chain=forward comment="drop src ipv6 bogons" \
    src-address-list=list-v6-bogons
add action=drop chain=forward comment="drop dst ipv6 bogons" \
    dst-address-list=list-v6-bogons
add action=drop chain=forward comment="rfc4890 drop hop-limit=1" hop-limit=\
    equal:1 protocol=icmpv6
add action=accept chain=forward comment="accept ICMPv6" protocol=icmpv6
add action=accept chain=forward comment="accept HIP" protocol=139
add action=accept chain=forward comment="accept IKE" dst-port=500,4500 \
    protocol=udp
add action=accept chain=forward comment="accept ipsec AH" protocol=ipsec-ah
add action=accept chain=forward comment="accept ipsec ESP" protocol=ipsec-esp
add action=accept chain=forward comment=\
    "accept all that matches ipsec policy" ipsec-policy=in,ipsec
add action=drop chain=forward comment=\
    "drop everything else not coming from LAN" in-interface-list=!iflist-lan
add action=accept chain=output comment="accept to list-v6-trusted" \
    dst-address-list=list-v6-trusted
/system clock
set time-zone-autodetect=no time-zone-name=Europe/London
/system identity
set name=fw-7t54
/system ntp client
set enabled=yes
/system ntp server
set enabled=yes
/system ntp client servers
add address=uk.pool.ntp.org
add address=162.159.200.1
add address=188.114.116.1
add address=162.159.200.123
add address=139.162.219.252
/system package update
set channel=testing
/system routerboard settings
set auto-upgrade=yes
/system script
add dont-require-permissions=no name=cacerts owner=dave policy=\
    ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="{\
    \r\
    \n  :do {\r\
    \n      /tool fetch url=https://mkcert.org/generate/ check-certificate=yes\
    \_dst-path=cacert.pem;\r\
    \n      /certificate remove [find];\r\
    \n      /certificate import file-name=cacert.pem passphrase=\"\";\r\
    \n      /file remove cacert.pem;\r\
    \n      :log info (\"Updated certificate trust store\");\r\
    \n  } on-error={\r\
    \n      :log error (\"Failed to update certificate trust store\");\r\
    \n  };\r\
    \n}"
/system watchdog
set watch-address=8.8.8.8
/tool mac-server
set allowed-interface-list=iflist-admin
/tool mac-server mac-winbox
set allowed-interface-list=iflist-admin
