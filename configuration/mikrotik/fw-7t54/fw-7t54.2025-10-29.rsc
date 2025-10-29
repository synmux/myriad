# 2025-10-29 16:26:34 by RouterOS 7.21beta3
# software id = H918-81CY
#
# model = RB4011iGS+5HacQ2HnD
# serial number = A283095904E8
/interface bridge
add admin-mac=B8:69:F4:E0:10:95 auto-mac=no igmp-snooping=yes name=external
add add-dhcp-option82=yes dhcp-snooping=yes igmp-snooping=yes name=internal
/interface ethernet
set [ find default-name=ether1 ] name=ether1-external
set [ find default-name=ether2 ] name=ether2-deeper-mini
set [ find default-name=ether3 ] name=ether3-deeper-pico
set [ find default-name=ether4 ] name=ether4-mbp
set [ find default-name=ether10 ] name=ether10-ipad
/interface list
add name=iflist-lan
/interface wifi channel
add band=5ghz-ac deprioritize-unii-3-4=yes disabled=no name=channel-deeper \
    skip-dfs-channels=all width=20mhz
/interface wifi configuration
add country="United Kingdom" disabled=no installation=indoor mode=ap \
    multicast-enhance=enabled name=config-deeper ssid=\
    deeper.wifi.lan.sl1p.net
/interface wifi security
add authentication-types=wpa2-psk disabled=no name=security-deeper \
    passphrase="packet hits a pocket"
/interface wifi
set [ find default-name=wifi1 ] channel=channel-deeper configuration=\
    config-deeper configuration.mode=ap disabled=no name=wifi security=\
    security-deeper
/ip pool
add name=dhcp-internal ranges=81.187.62.80-81.187.62.90
/ip dhcp-server
add add-arp=yes address-pool=dhcp-internal interface=internal lease-time=10m \
    name=dhcp-internal support-broadcom-tr101=yes
/interface l2tp-client
add add-default-route=yes connect-to=l2tp.aa.net.uk default-route-distance=20 \
    disabled=no name=l2tp-aaisp password=ElatedAmuletElective profile=default \
    user=dw121@a.2
/zerotier
set zt-central disabled=no disabled=no identity="0007da3940:0:fd19994617b2dbcb\
    e42c2217503ca1a2209536b1b6a5d38f2e301acea64d0b6641af115aa4f44731d7a714fae4\
    f372790fa0b4f3605baef0e47245f8ab4cfc1c:1b151bb0e3a55e02f9cee0b3246bae10a5c\
    4d95ce9fceb2355d499aaf348d7662484396c66a922abca5203991cd985b585c98bca43742\
    7b4ade05cf0d62367d2" name=zt-central route-distance=10
/zerotier interface
add allow-default=no allow-global=no allow-managed=yes disabled=no instance=\
    zt-central name=zt-backplane network=8bd5124fd63a0d47
#error exporting "/app/settings"
/interface bridge port
add bridge=external interface=ether1-external
add bridge=internal interface=ether2-deeper-mini
add bridge=internal interface=ether3-deeper-pico
add bridge=internal interface=ether4-mbp
add bridge=internal interface=ether5
add bridge=internal interface=ether6
add bridge=internal interface=ether7
add bridge=internal interface=ether8
add bridge=internal interface=ether9
add bridge=external interface=ether10-ipad
add bridge=internal interface=sfp-sfpplus1
add bridge=internal interface=wifi
/ip firewall connection tracking
set udp-timeout=10s
/interface list member
add interface=internal list=iflist-lan
add interface=zt-backplane list=iflist-lan
/interface wifi cap
set discovery-interfaces=external slaves-datapath=*1
/ip address
add address=81.187.62.65/27 interface=internal network=81.187.62.64
/ip dhcp-client
add default-route-distance=30 interface=external use-peer-dns=no
/ip dhcp-server lease
add address=81.187.62.71 comment="deeper pico" mac-address=02:00:0C:90:26:CD \
    server=dhcp-internal
add address=81.187.62.70 comment="deeper mini" mac-address=B0:C9:DA:1E:2C:73 \
    server=dhcp-internal
add address=81.187.62.72 comment="deeper air" mac-address=F0:A8:82:63:F0:BE \
    server=dhcp-internal
add address=81.187.62.73 client-id=1:80:3f:5d:fe:6d:9a mac-address=\
    80:3F:5D:FE:6D:9A server=dhcp-internal
/ip dhcp-server network
add address=81.187.62.64/27 dns-server=8.8.8.8,8.8.4.4 gateway=81.187.62.65 \
    ntp-server=81.187.62.65
/ip dns
set servers=8.8.8.8,8.8.4.4
/ip firewall address-list
add address=0.0.0.0/8 comment=this-network list=list-v4-bogons
add address=100.64.0.0/10 comment=cgn list=list-v4-bogons
add address=127.0.0.0/8 comment=loopback list=list-v4-bogons
add address=127.0.53.53 comment=name-collision-occurrence list=list-v4-bogons
add address=169.254.0.0/16 comment=link-local list=list-v4-bogons
add address=192.0.0.0/24 comment=ietf-proto list=list-v4-bogons
add address=192.0.2.0/24 comment=test-net-1 list=list-v4-bogons
add address=192.88.99.0/24 comment=6to4-relay-anycast list=list-v4-bogons
add address=198.18.0.0/15 comment=interconnect-benchmarking list=\
    list-v4-bogons
add address=198.51.100.0/24 comment=test-net-2 list=list-v4-bogons
add address=203.0.113.0/24 comment=test-net-3 list=list-v4-bogons
add address=224.0.0.0/4 comment=multicast list=list-v4-bogons
add address=240.0.0.0/4 comment=reserved list=list-v4-bogons
add address=255.255.255.255 comment=broadcast list=list-v4-bogons
add address=10.0.0.0/8 comment=private:10.0.0.0/8 list=list-v4-private
add address=172.16.0.0/12 comment=private:172.16.0.0/12 list=list-v4-private
add address=192.168.0.0/16 comment=private:192.168.0.0/16 list=\
    list-v4-private
add address=81.187.62.64/27 comment=private:81.187.62.64/27 list=\
    list-v4-private
/ip firewall filter
add action=accept chain=input comment=input:accept disabled=yes
add action=accept chain=forward comment=forward:accept disabled=yes
add action=accept chain=output comment=output:accept disabled=yes
add action=jump chain=input comment=input:jump:conntracked jump-target=\
    conntracked
add action=jump chain=input comment=input:jump:bogons jump-target=bogons
add action=jump chain=input comment=input:jump:accepts jump-target=accepts
add action=accept chain=input dst-port=212 protocol=tcp
add action=accept chain=input src-address-list=list-v4-private
add action=drop chain=input comment=input:policy:drop
add action=jump chain=forward comment=forward:jump:conntracked jump-target=\
    conntracked
add action=jump chain=forward comment=forward:jump:bogons jump-target=bogons
add action=jump chain=forward comment=forward:jump:drops jump-target=drops
add action=accept chain=forward comment=forward:policy:accept
add action=jump chain=output comment=output:jump:conntracked jump-target=\
    conntracked
add action=jump chain=output comment=output:jump:bogons jump-target=bogons
add action=accept chain=output comment=output:policy:accept
add action=drop chain=bogons comment=bogons:drop:connection-state:invalid \
    connection-state=invalid
add action=drop chain=bogons comment=bogons:drop:src-address \
    src-address-list=list-v4-bogons
add action=drop chain=bogons comment=bogons:drop:dst-address \
    dst-address-list=list-v4-bogons
add action=return chain=bogons comment=bogons:return
add action=accept chain=accepts protocol=igmp
add action=accept chain=accepts comment="echo reply" icmp-options=0:0 \
    protocol=icmp
add action=accept chain=accepts comment="net unreachable" icmp-options=3:0 \
    protocol=icmp
add action=accept chain=accepts comment="host unreachable" icmp-options=3:1 \
    protocol=icmp
add action=accept chain=accepts comment=\
    "host unreachable fragmentation required" icmp-options=3:4 protocol=icmp
add action=accept chain=accepts comment="allow echo request" icmp-options=8:0 \
    protocol=icmp
add action=accept chain=accepts comment="allow time exceed" icmp-options=11:0 \
    protocol=icmp
add action=accept chain=accepts comment="allow parameter bad" icmp-options=\
    12:0 protocol=icmp
add action=return chain=accepts
add action=drop chain=drops dst-port=53 protocol=udp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=69 protocol=udp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=137-139 protocol=udp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=161-162 protocol=udp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=20-21 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=22 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=23 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=25 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=80 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=110 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=137-139 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=143 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=389 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=443 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=445 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=587 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=636 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=993 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=995 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=1433 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=1521 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=3306 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=3389 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=5432 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=5900-5901 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=6379 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=8080 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=8291 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=9200 protocol=tcp src-address=\
    !81.187.62.64/27
add action=drop chain=drops dst-port=27017 protocol=tcp src-address=\
    !81.187.62.64/27
add action=return chain=drops
add action=fasttrack-connection chain=conntracked comment=\
    conntracked:fasttrack:eru connection-state=established,related,untracked
add action=accept chain=conntracked comment=conntracked:accept:eru \
    connection-state=established,related,untracked
add action=return chain=conntracked comment=conntracked:return
/ip firewall nat
add action=masquerade chain=srcnat comment=nat:msq:mgmt ipsec-policy=out,none \
    out-interface-list=iflist-lan src-address=10.50.50.0/24
add action=masquerade chain=srcnat comment=nat:msq:zt-mgmt ipsec-policy=\
    out,none out-interface-list=iflist-lan src-address=192.168.204.0/24
add action=masquerade chain=srcnat comment=nat:msq:mgmt ipsec-policy=out,none \
    out-interface-list=iflist-lan src-address=10.50.50.0/24
add action=masquerade chain=srcnat comment=nat:msq:zt-mgmt ipsec-policy=\
    out,none out-interface-list=iflist-lan src-address=192.168.204.0/24
/ip firewall service-port
set irc disabled=no
set rtsp disabled=no
/ip service
set telnet disabled=yes
set www disabled=yes
set ssh port=212
set www-ssl certificate=self-signed disabled=no
set api disabled=yes
set api-ssl certificate=self-signed disabled=yes
/ip service webserver
set acme-plain=no crl-plain=no graphs-plain=no index-plain=no rest-plain=no \
    scep-plain=no webfig-plain=no
/ip ssh
set forwarding-enabled=both host-key-type=ed25519 password-authentication=no \
    strong-crypto=yes
/ipv6 dhcp-client
add add-default-route=yes interface=l2tp-aaisp pool-name=poolv6-aaisp \
    pool-prefix-length=60 request=address use-peer-dns=no
/ipv6 firewall address-list
add address=::/128 comment=unicast:unspecified:node-scope list=list-v6-bogons
add address=::1/128 comment=unicast:loopback:node-scope list=list-v6-bogons
add address=::ffff:0.0.0.0/96 comment=ipv4:mapped list=list-v6-bogons
add address=::/96 comment=ipv4:compat list=list-v6-bogons
add address=100::/64 comment=blackhole list=list-v6-bogons
add address=2001:10::/28 comment=orchid list=list-v6-bogons
add address=2001:db8::/32 comment=documentation list=list-v6-bogons
add address=2002::/24 comment=6to4:0.0.0.0/8 list=list-v6-v4-bogons
add address=2002:7f00::/24 comment=6to4:127.0.0.0/8 list=list-v6-v4-bogons
add address=2002:a9fe::/32 comment=6to4:169.254.0.0/16 list=list-v6-v4-bogons
add address=2002:c000::/40 comment=6to4:192.0.0.0/24 list=list-v6-v4-bogons
add address=2002:c000:200::/40 comment=6to4:192.0.2.0/24 list=\
    list-v6-v4-bogons
add address=2002:c612::/31 comment=6to4:198.18.0.0/15 list=list-v6-v4-bogons
add address=2002:c633:6400::/40 comment=6to4:198.51.100.0/24 list=\
    list-v6-v4-bogons
add address=2002:cb00:7100::/40 comment=6to4:203.0.113.0/24 list=\
    list-v6-v4-bogons
add address=2002:e000::/20 comment=6to4:224.0.0.0/4 list=list-v6-v4-bogons
add address=2002:f000::/20 comment=6to4:240.0.0.0/4 list=list-v6-v4-bogons
add address=2002:ffff:ffff::/48 comment=6to4:255.255.255.255/32 list=\
    list-v6-v4-bogons
add address=2001::/40 comment=teredo:0.0.0.0/8 list=list-v6-v4-bogons
add address=2001:0:7f00::/40 comment=teredo:127.0.0.0/8 list=\
    list-v6-v4-bogons
add address=2001:0:a9fe::/48 comment=teredo:169.254.0.0/16 list=\
    list-v6-v4-bogons
add address=2001:0:c000::/56 comment=teredo:192.0.0.0/24 list=\
    list-v6-v4-bogons
add address=2001:0:c000:200::/56 comment=teredo:192.0.2.0/24 list=\
    list-v6-v4-bogons
add address=2001:0:c612::/47 comment=teredo:198.18.0.0/15 list=\
    list-v6-v4-bogons
add address=2001:0:c633:6400::/56 comment=teredo:198.51.100.0/24 list=\
    list-v6-v4-bogons
add address=2001:0:cb00:7100::/56 comment=teredo:203.0.113.0/24 list=\
    list-v6-v4-bogons
add address=2001:0:e000::/36 comment=teredo:224.0.0.0/4 list=\
    list-v6-v4-bogons
add address=2001:0:f000::/36 comment=teredo:240.0.0.0/4 list=\
    list-v6-v4-bogons
add address=2001:0:ffff:ffff::/64 comment=teredo:255.255.255.255/32 list=\
    list-v6-v4-bogons
add address=fc00::/7 comment=ula list=list-v6-v4-private
add address=fe80::/10 comment=unicast:link-local list=list-v6-v4-private
add address=fec0::/10 comment="unicast:site-local(deprecated)" list=\
    list-v6-v4-private
add address=ff00::/16 comment="multicast(ff0e:/16:global)" list=\
    list-v6-v4-private
add address=2002:a00::/24 comment=6to4:10.0.0.0/8 list=list-v6-v4-private
add address=2002:ac10::/28 comment=6to4:172.16.0.0/12 list=list-v6-v4-private
add address=2002:c0a8::/32 comment=6to4:192.168.0.0/16 list=\
    list-v6-v4-private
add address=2001:0:a00::/40 comment=teredo:10.0.0.0/8 list=list-v6-v4-private
add address=2001:0:ac10::/44 comment=teredo:172.16.0.0/12 list=\
    list-v6-v4-private
add address=2001:0:c0a8::/48 comment=teredo:192.168.0.0/16 list=\
    list-v6-v4-private
/ipv6 firewall filter
add action=accept chain=input comment=input:accept disabled=yes
add action=accept chain=output comment=forward:accept disabled=yes
add action=accept chain=forward comment=output:accept disabled=yes
add action=jump chain=input comment=input:jump:bogons jump-target=bogons
add action=jump chain=input comment=input:jump:accepts jump-target=accepts
add action=jump chain=input comment=input:jump:conntracked jump-target=\
    conntracked
add action=accept chain=input comment=input:accept:dhcpv6-pd dst-port=546 \
    protocol=udp src-address=fe80::/10
add action=accept chain=input comment=input:accept:dns dst-port=53 protocol=\
    udp
add action=accept chain=input comment=input:accept:ntp dst-port=123 protocol=\
    udp
add action=accept chain=input comment=input:accept:ssh-alt dst-port=212 \
    protocol=tcp
add action=accept chain=input comment=input:accept:winbox dst-port=8291 \
    protocol=tcp
add action=drop chain=input comment=input:drop:policy
add action=jump chain=forward comment=forward:jump:bogons jump-target=bogons
add action=jump chain=forward comment=forward:jump:accepts jump-target=\
    accepts
add action=jump chain=forward comment=forward:jump:conntracked jump-target=\
    conntracked
add action=accept chain=forward comment=forward:accept:ipsec:in,ipsec \
    ipsec-policy=in,ipsec
add action=accept chain=forward comment=forward:accept:ipsec:in,ipsec \
    ipsec-policy=out,ipsec
add action=accept chain=forward comment=\
    "forward:accept:icmpv6:hop-limit!=1(rfc4890)" hop-limit=not-equal:1 \
    protocol=icmpv6
add action=accept chain=forward comment=forward:accept:hip protocol=139
add action=accept chain=forward comment=forward:accept:ike dst-port=500,4500 \
    protocol=udp
add action=accept chain=forward comment=forward:accept:ipsec-ah protocol=\
    ipsec-ah
add action=accept chain=forward comment=forward:accept:ipsec-esp protocol=\
    ipsec-esp
add action=accept chain=forward comment=forward:accept:iflist-lan \
    in-interface-list=iflist-lan
add action=drop chain=forward comment=forward:drop:policy log-prefix=\
    ipv6-forward-drop
add action=jump chain=output comment=output:jump:bogons jump-target=bogons
add action=jump chain=output comment=output:jump:accepts jump-target=accepts
add action=jump chain=output comment=output:jump:conntracked jump-target=\
    conntracked
add action=accept chain=output comment=output:accept:policy
add action=drop chain=bogons comment=bogons:drop:connection-state:invalid \
    connection-state=invalid
add action=drop chain=bogons comment=bogons:drop:v6:src-address \
    src-address-list=list-v6-bogons
add action=drop chain=bogons comment=bogons:drop:v6:dst-address \
    dst-address-list=list-v6-bogons
add action=drop chain=bogons comment=bogons:drop:v6-v4:src-address \
    src-address-list=list-v6-v4-bogons
add action=drop chain=bogons comment=bogons:drop:v6-v4:dst-address \
    dst-address-list=list-v6-v4-bogons
add action=return chain=bogons comment=bogons:return
add action=accept chain=accepts comment=accepts:accept:icmpv6 protocol=icmpv6
add action=accept chain=accepts comment=accepts:accept:ike dst-port=500,4500 \
    protocol=udp
add action=accept chain=accepts comment=accepts:accept:ipsec-ah protocol=\
    ipsec-ah
add action=accept chain=accepts comment=accepts:accept:ipsec-esp protocol=\
    ipsec-esp
add action=accept chain=accepts comment=accepts:accept:traceroute port=\
    33434-33534 protocol=udp
add action=return chain=accepts comment=accepts:return
add action=accept chain=conntracked comment=conntracked:accept:eru \
    connection-state=established,related,untracked
add action=return chain=conntracked comment=conntracked:return
/system clock
set time-zone-name=Europe/London
/system identity
set name=fw-7t54
/system package update
set channel=testing
/system routerboard settings
set auto-upgrade=yes
