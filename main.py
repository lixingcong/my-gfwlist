#!/usr/bin/env python
# -*- coding: utf-8 -*-

# lixingcong@live.com
# Generate domains for dnsmasq-regex
# support for server or ipset block

import argparse
import datetime
import sys

CONFIG_COMMENT='#'
CONFIG_NEWLINE='\n'
DEFAULT_NAMESERVER='8.8.8.8'

ONLY_MODE_NAMESERVER  = 0x01
ONLY_MODE_IPSET       = 0x10
ONLY_MODE_BOTH        = ONLY_MODE_NAMESERVER | ONLY_MODE_IPSET

def generate_a_config(filename_in, filename_out, nameserver, ipset_name, is_noRegex, only_mode):
	domain_list=[]
	
	# Read from file
	with open(filename_in, 'r') as f:
		for line in f.read().splitlines():
			line_trimed=line.strip()
			if len(line_trimed) == 0 or line_trimed[0] == CONFIG_COMMENT:
				continue
			
			if is_noRegex is True and line_trimed[0] == ':' and line_trimed[-1] == ':':
				print '[INFO] ignore regex domain: '+ line_trimed
				continue
			
			domain_list.append(line_trimed)
	
	# Write to file
	with open(filename_out, 'w') as f:
		time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		item_count_str = 'total: '+str(len(domain_list))
		noRegex_str=' (no-regex)' if is_noRegex is True else ''
		
		f.write(CONFIG_COMMENT+time_str+CONFIG_NEWLINE)
		f.write(CONFIG_COMMENT+item_count_str+noRegex_str+CONFIG_NEWLINE)
		
		for domain in domain_list:
			if only_mode & ONLY_MODE_NAMESERVER == ONLY_MODE_NAMESERVER:
				f.write('server=/' + domain + '/' + nameserver + CONFIG_NEWLINE)
			
			if ipset_name is not None and (only_mode & ONLY_MODE_IPSET == ONLY_MODE_IPSET):
				f.write('ipset=/' + domain + '/' + ipset_name + CONFIG_NEWLINE)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='tool',
								     formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=80),
								     description='A simple config file generator for dnsmasq-regex')
	
	parser.add_argument('-i','--input', help='filename input', required=True)
	parser.add_argument('-o','--output', help='filename output', required=True)
	
	parser.add_argument('-n','--nameserver', help='nameserver to resolve, default: '+DEFAULT_NAMESERVER, default=DEFAULT_NAMESERVER, required=False)
	parser.add_argument('-s','--ipset-name', help='ipset name to add', default=None, required=False)
	
	parser.add_argument('-N','--nameserver-only', help='generate nameserver only', action='store_true')
	parser.add_argument('-S','--ipset-only', help='generate ipset only', action='store_true')
	
	parser.add_argument('-R','--no-regex', help='ignore regex domains', action='store_true')
	args = vars(parser.parse_args())
	
	if args['ipset_only'] is True and args['nameserver_only'] is True:
		print '[ERROR] conflict option --ipset-only and --nameserver-only'
		sys.exit(-1)
	
	# default mode
	only_mode = ONLY_MODE_BOTH
	
	if args['nameserver_only'] is True:
		only_mode = ONLY_MODE_NAMESERVER
	elif args['ipset_only'] is True:
		only_mode = ONLY_MODE_IPSET
	
	generate_a_config(args['input'],args['output'],args['nameserver'],args['ipset_name'],args['no_regex'],only_mode)
	
