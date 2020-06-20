#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# lixingcong@live.com
# Generate ad domains for dnsmasq

import argparse
import datetime

CONFIG_COMMENT='#'
CONFIG_NEWLINE='\n'

def generate_a_config(filename_in, filename_out):
	domain_list=[]
	
	# Read from file
	with open(filename_in, 'r') as f:
		for line in f.read().splitlines():
			line_trimed=line.strip()
			if len(line_trimed) == 0 or line_trimed[0] == CONFIG_COMMENT:
				continue
			
			domain_list.append(line_trimed)
	
	# Write to file
	with open(filename_out, 'w') as f:
		time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		item_count_str = 'total: '+str(len(domain_list))
		
		f.write(CONFIG_COMMENT+time_str+CONFIG_NEWLINE)
		f.write(CONFIG_COMMENT+item_count_str+CONFIG_NEWLINE)
		
		for domain in domain_list:
			f.write('address=/' + domain + '/' + CONFIG_NEWLINE)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='tool',
	                                 formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=80),
	                                 description='A simple config file generator for dnsmasq')
	
	parser.add_argument('-i','--input', help='filename input', required=True)
	parser.add_argument('-o','--output', help='filename output', required=True)

	args = vars(parser.parse_args())
	
	generate_a_config(args['input'],args['output'])
	
