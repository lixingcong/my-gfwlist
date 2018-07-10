#!/usr/bin/env python
# -*- coding: utf-8 -*-

# lixingcong@live.com
# Generate domains for dnsmasq-regex
# support for server or ipset block

import argparse
import datetime

CONFIG_COMMENT='#'
CONFIG_NEWLINE='\n'
DEFAULT_NAMESERVER='8.8.8.8'

def generate_a_config(filename_in, filename_out, nameserver, ipset_name, is_noRegex):
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
			f.write('server=/' + domain + '/' + nameserver + CONFIG_NEWLINE)
			
			if ipset_name is not None:
				f.write('ipset=/' + domain + '/' + ipset_name + CONFIG_NEWLINE)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='A simple config file generator for dnsmasq-regex')
	parser.add_argument('-i','--input', help='filename input', required=True)
	parser.add_argument('-o','--output', help='filename output', required=True)
	parser.add_argument('-n','--nameserver', help='nameserver to resolve, default: '+DEFAULT_NAMESERVER, default=DEFAULT_NAMESERVER, required=False)
	parser.add_argument('-s','--ipset-name', help='ipset name to add', default=None, required=False)
	parser.add_argument('-N','--no-regex', help='ignore regex domains(disable ipset also)', action='store_true')
	args = vars(parser.parse_args())
	
	# Overwrite ipset name
	if args['no_regex'] is True and args['ipset_name'] is not None:
		print '[WARNING] ipset was disable due to no regex'
		args['ipset_name']=None

	generate_a_config(args['input'],args['output'],args['nameserver'],args['ipset_name'],args['no_regex'])
	
