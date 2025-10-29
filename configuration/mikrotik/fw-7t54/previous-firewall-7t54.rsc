# 2025-10-28 18:42:10 by RouterOS 7.21beta3
# software id = H918-81CY
#
# model = RB4011iGS+5HacQ2HnD
# serial number = A283095904E8

/ip firewall filter remove [find where !dynamic]
/ip firewall filter
add action=passthrough chain=forward connection-mark=suspicious log=yes \
    log-prefix=suspicious
add action=accept chain=input comment=input:accept disabled=yes
add action=accept chain=forward comment=forward:accept disabled=yes
add action=accept chain=output comment=output:accept disabled=yes
add action=jump chain=input comment=input:jump:conntracked jump-target=\
    conntracked
add action=jump chain=input comment=input:jump:bogons jump-target=bogons
add action=jump chain=input comment=input:jump:accepts jump-target=accepts
add action=accept chain=input dst-port=123 protocol=udp
add action=accept chain=input dst-port=212 protocol=tcp
add action=accept chain=input dst-port=8291 protocol=tcp
add action=accept chain=input in-interface-list=iflist-lan
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
add action=jump chain=accepts jump-target=icmp protocol=icmp
add action=accept chain=accepts protocol=igmp
add action=return chain=accepts
add action=reject chain=drops dst-port=53 protocol=udp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=69 protocol=udp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=137-139 protocol=udp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=161-162 protocol=udp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=20-21 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=22 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=23 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=25 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=80 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=110 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=137-139 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=143 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=389 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=443 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=445 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=587 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=636 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=993 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=995 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=1433 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=1521 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=3306 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=3389 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=5432 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=5900-5901 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=6379 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=8080 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=8291 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=9200 protocol=tcp src-address=\
    !81.187.62.64/27
add action=reject chain=drops dst-port=27017 protocol=tcp src-address=\
    !81.187.62.64/27
add action=return chain=drops
add action=fasttrack-connection chain=conntracked comment=\
    conntracked:fasttrack:eru connection-state=established,related,untracked
add action=accept chain=conntracked comment=conntracked:accept:eru \
    connection-state=established,related,untracked
add action=return chain=conntracked comment=conntracked:return
add action=accept chain=icmp comment="echo reply" icmp-options=0:0 protocol=\
    icmp
add action=accept chain=icmp comment="net unreachable" icmp-options=3:0 \
    protocol=icmp
add action=accept chain=icmp comment="host unreachable" icmp-options=3:1 \
    protocol=icmp
add action=accept chain=icmp comment=\
    "host unreachable fragmentation required" icmp-options=3:4 protocol=icmp
add action=accept chain=icmp comment="allow echo request" icmp-options=8:0 \
    protocol=icmp
add action=accept chain=icmp comment="allow time exceed" icmp-options=11:0 \
    protocol=icmp
add action=accept chain=icmp comment="allow parameter bad" icmp-options=12:0 \
    protocol=icmp
add action=return chain=icmp comment=icmp:return
add action=accept chain=forward connection-mark=suspicious
/ip firewall mangle remove [find where !dynamic]
/ip firewall mangle
add action=mark-connection chain=prerouting dst-address=81.187.62.64/27 \
    dst-address-list=list-v4-bogons dst-port=23 new-connection-mark=\
    suspicious protocol=tcp src-address=!81.187.62.64/27
/ip firewall nat
add action=masquerade chain=srcnat comment=nat:msq:mgmt ipsec-policy=out,none \
    out-interface-list=iflist-lan src-address=10.50.50.0/24
add action=masquerade chain=srcnat comment=nat:msq:zt-mgmt ipsec-policy=\
    out,none out-interface-list=iflist-lan src-address=192.168.204.0/24
/ip firewall service-port
set irc disabled=no
set rtsp disabled=no
