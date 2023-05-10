# Generate my gfwlist for dnsmasq

I hate DNS spoofing. Here is a simple script to ouput the configuration for some domains which were polluted.

## Prerequisites

Use a patched version [dnsmasq-regex](https://github.com/lixingcong/dnsmasq-regex) to get regex support.

Make sure you had compiled dnsmasq with these flags: ```regex(+ipset)```

```
$ dnsmasq -v
Dnsmasq version 2.80  Copyright (c) 2000-2018 Simon Kelley
Compile time options: IPv6 GNU-getopt no-DBus no-i18n regex(+ipset) no-IDN DHCP DHCPv6 no-Lua TFTP no-conntrack ipset auth no-DNSSEC loop-detect inotify

```

If you do not have dnsmasq-regex, it is ok. You need to write your custom domain list(the list may be a bit longer than the regex verison) and pass argument '--no-regex' to script for ignoring those regex domains.

## Usage

```
$ python3 generate_config.py --help
usage: generate_config.py [-h] -f FILE -p PREFIX -s SUFFIX [-R]

A simple config file generator for dnsmasq

options:
  -h, --help                  show this help message and exit
  -f FILE, --file FILE        file path to input
  -p PREFIX, --prefix PREFIX  prefix to be inserted to each line
  -s SUFFIX, --suffix SUFFIX  suffix to be appended to each line
  -R, --no-regex              ignore regex domains
```

Example

```
python3 generate_config.py -f domains/ad.txt --prefix server=/ --suffix /1.1.1.1
```

The script will read 'domains/ad.txt' and print each line with prefix and suffix like this:

```
server=/:.*google-analytics\.com:/1.1.1.1
server=/:.*googlesyndication\.com:/1.1.1.1
server=/:.*googletagservices\.com:/1.1.1.1
```

## Advanced applications

Here are some tricks we could play with dnsmasq-regex.

### Work with shadowsocks-libev

It is a good practice to use ss-redir to bypass the Great Firewall.

To get ipset config works, you need to create a set named 'gfwlist' first. You must run with sudo :)

```
ipset create gfwlist hash:ip
```

Use the scirpt to generate full nameserver and ipset config file.

```
python3 generate_config.py -f domains/gfw_blocked.txt --prefix server=/ --suffix /1.1.1.1
python3 generate_config.py -f domains/gfw_blocked.txt --prefix ipset=/ --suffix /gfwlist
```

Save the script outputs to file ```/tmp/domains_blocked.conf```

Run dnsmasq as your system resolver. Run ss-redir listening on port 1234. You must run dnsmasq with root to modify ipset.

```
dnsmasq --conf-file=/tmp/domains_blocked.conf
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
