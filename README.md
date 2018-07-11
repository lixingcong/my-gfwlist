# Generate my gfwlist for dnsmasq

I hate DNS spoofing. Here is a simple script to ouput the configuration for some domains which were poisoned.

## Prerequisites

Use a patched version [dnsmasq-regex](https://github.com/lixingcong/dnsmasq-regex) to get regex support.

Make sure compile dnsmasq with these flags: ```regex```and```ipset```

```
$ dnsmasq -v
Dnsmasq version 2.80test2  Copyright (c) 2000-2018 Simon Kelley
Compile time options: IPv6 GNU-getopt no-DBus no-i18n regex no-IDN DHCP DHCPv6 no-Lua TFTP no-conntrack ipset auth no-DNSSEC loop-detect inotify

```

If you do not have dnsmasq-regex, it is ok. You need you write your custom domain list(the list may be a bit longer than regex verison) and pass argument '--no-regex' to main.py for ignoring those regex domains.

## Usage

```
$ python main.py -h
usage: tool [-h] -i INPUT -o OUTPUT [-n NAMESERVER] [-s IPSET_NAME] [-N] [-S] [-R]

A simple config file generator for dnsmasq-regex

optional arguments:
  -h, --help                              show this help message and exit
  -i INPUT, --input INPUT                 filename input
  -o OUTPUT, --output OUTPUT              filename output
  -n NAMESERVER, --nameserver NAMESERVER  nameserver to resolve, default: 8.8.8.8
  -s IPSET_NAME, --ipset-name IPSET_NAME  ipset name to add
  -N, --nameserver-only                   generate nameserver only
  -S, --ipset-only                        generate ipset only
  -R, --no-regex                          ignore regex domains
```

Example

```
python main.py -i domains.txt -o /tmp/gfwlist.conf -n 8.8.8.8#53 -s gfwlist
```

The script output basic server configuration and ipset.

```
cat /tmp/gfwlist.conf

server=/facebook.com/8.8.8.8#53
ipset=/facebook.com/gfwlist
server=/google.com/8.8.8.8#53
ipset=/google.com/gfwlist
```

## Advanced applications

Here are some tricks we could play with dnsmasq-regex.

### Work with shadowsocks-libev

It is a good practice to use ss-redir to bypass the Great Firewall.

To get ipset config works, you need to create a set named 'gfwlist' first.

```
ipset create gfwlist hash:ip
```

Use the scirpt 'main.py' above to generate full nameserver and ipset config file.

Run dnsmasq as your system resolver. Run ss-redir listening on port 1234.

```
dnsmasq --conf-dir=/tmp/gfwlist.conf
ss-redir -c /path/to/config.json -l 1234 -f /tmp/ss.pid
```

Use iptables to redirect traffic which dest ip were matched in ipset gfwlist. Assume your IP of ss-server is 123.123.123.123.

```
# Create chain
iptables -t nat -N SHADOWSOCKS

# Ignore special dest IP
iptables -t nat -A SHADOWSOCKS -d 123.123.123.123 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 0.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 10.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 127.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 169.254.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 172.16.0.0/12 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 192.168.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 224.0.0.0/4 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 240.0.0.0/4 -j RETURN

# Redirect gfwlist
iptables -t nat -A SHADOWSOCKS -p tcp -m set --match-set gfwlist dst -j REDIRECT --to-ports 1234

# Apply chain to table
iptables -t nat -A OUTPUT -p tcp -j SHADOWSOCKS
```

Now you are already done. Visit the websites you generated right now!

If you want to shutdown the service of ipset and iptables(destroy the rules), just flush the chain.

```
# Delete the rules
iptables -t nat -D OUTPUT -p tcp -j SHADOWSOCKS
iptables -t nat -F SHADOWSOCKS
iptables -t nat -X SHADOWSOCKS

# Delete the set
ipset destroy gfwlist

# Kill ss-redir
killall ss-redir
```

### Resctrict visiting some bad websites

It has the similar setup to the last chapter, just modify your iptables script to DROP those traffic matched ipset.

```
iptables -A OUTPUT -p tcp -m set --match-set gfwlist dst -j DROP
```
