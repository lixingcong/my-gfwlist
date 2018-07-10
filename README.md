# Generate my gfwlist for dnsmasq

I hate DNS spoofing. Here is a simple script to ouput the configuration for some domains which were poisoned.

## Prerequisites

Use a patched version [dnsmasq-regex](https://github.com/lixingcong/dnsmasq-regex) to get regex support.

If you do not have one, it is ok. You need you write your custom domain list(the list may be a bit longer than regex verison) and pass argument '--no-regex' to main.py for ignoring those regex domains.

## Usage

```
$ python main.py --help
usage: main.py [-h] -i INPUT -o OUTPUT [-n NAMESERVER] [-s IPSET_NAME] [-N]

A simple config file generator for dnsmasq-regex

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        filename input
  -o OUTPUT, --output OUTPUT
                        filename output
  -n NAMESERVER, --nameserver NAMESERVER
                        nameserver to resolve, default: 8.8.8.8
  -s IPSET_NAME, --ipset-name IPSET_NAME
                        ipset name to add
  -N, --no-regex        ignore regex domains(disable ipset also)
```

Example

```
python main.py -i domains.txt -o /tmp/out.txt -n 8.8.8.8#53
```
