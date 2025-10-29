# 2025-10-28 14:52:39 by RouterOS 7.21beta3
# software id = H918-81CY
#
# model = RB4011iGS+5HacQ2HnD
# serial number = A283095904E8

/ip firewall filter
/ip firewall filter remove [find where !dynamic]

add action=accept chain=input comment=input:accept disabled=yes
add action=accept chain=forward comment=forward:accept disabled=yes
add action=accept chain=output comment=output:accept disabled=yes
add action=jump chain=input comment=input:jump:accepts jump-target=accepts
add action=accept chain=input dst-port=212 protocol=tcp
add action=accept chain=input in-interface-list=iflist-lan
add action=drop chain=input comment=input:policy:drop
add action=jump chain=forward comment=forward:jump:conntracked jump-target=conntrackedbogons
add action=reject chain=forward connection-mark=suspicious
add action=accept chain=forward comment=forward:policy:accept
add action=accept chain=output comment=output:policy:accept
add action=accept chain=accepts comment="echo reply" icmp-options=0:0 protocol=icmp
add action=accept chain=accepts comment="net unreachable" icmp-options=3:0 protocol=icmp
add action=accept chain=accepts comment="host unreachable" icmp-options=3:1 protocol=icmp
add action=accept chain=accepts comment="host unreachable fragmentation required" icmp-options=3:4 protocol=icmp
add action=accept chain=accepts comment="allow echo request" icmp-options=8:0 protocol=icmp
add action=accept chain=accepts comment="allow time exceed" icmp-options=11:0 protocol=icmp
add action=accept chain=accepts comment="allow parameter bad" icmp-options=12:0 protocol=icmp
add action=accept chain=accepts protocol=igmp
add action=return chain=accepts
add action=fasttrack-connection chain=conntracked comment=conntracked:fasttrack:eru connection-state=established,related,untracked
add action=accept chain=conntracked comment=conntracked:accept:eru connection-state=established,related,untracked
add action=return chain=conntracked comment=conntracked:return

/ip firewall mangle
/ip firewall mangle remove [find where !dynamic]

add chain=forward action=mark-connection new-connection-mark=suspicious connection-state=invalid passthrough=yes
add chain=forward action=mark-connection new-connection-mark=suspicious src-address-list=list-v4-bogons passthrough=yes
add chain=forward action=mark-connection new-connection-mark=suspicious dst-address-list=list-v4-bogons passthrough=yes
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=20-21
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=22
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=23
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=25
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=80
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=110
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=137-139
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=143
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=389
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=443
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=445
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=587
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=636
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=993
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=995
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=1433
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=1521
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=3306
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=3389
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=5432
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=5900-5910
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=6379
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=8080
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=8291
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=9200
add chain=forward action=mark-connection new-connection-mark=suspicious passthrough=yes protocol=tcp src-address=!81.187.62.64/27 dst-address=81.187.62.64/27 dst-port=27017
