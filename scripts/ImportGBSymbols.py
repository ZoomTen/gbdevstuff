# Imports an RGBASM SYM file and creates labels / functions out of them.
# @author Zumi
# @category Symbol
#

from ghidra.program.model.symbol.SourceType import *
import string
import re

functionManager = currentProgram.getFunctionManager()

f = askFile("Open a .sym file...", "Go!")

is_ram = False

for line in file(f.absolutePath):  # note, cannot use open(), since that is in GhidraScript
	pieces = line.split()

	if pieces[0] != ';':
		addr, sym = tuple(pieces[0:2])
		
		gb_addr = re.match(r'([0-9a-fA-F]{2}):([0-9a-fA-F]{4})', addr)
		
		if gb_addr:
			_bank, _addr = tuple([x.lower() for x in list(gb_addr.groups())])
			if re.match(r'[cd][0-9a-f]{2}', _addr):
				address_string = '{}'.format(_addr)
				is_ram = True
			elif re.match(r'[89][0-9a-f]{2}', _addr):
				address_string = '{}'.format(_addr)
				is_ram = True
			elif re.match(r'[ab][0-9a-f]{2}', _addr):
				address_string = '{}'.format(_addr)
				is_ram = True
			elif re.match(r'fe[0-9][0-9a-f]', _addr):
				address_string = '{}'.format(_addr)
				is_ram = True
			elif re.match(r'ffff', _addr):
				is_ram = True
				pass
			elif re.match(r'ff[0-9a-f][0-9a-f]', _addr):
				address_string = '{}'.format(_addr)
				is_ram = True
			else:
				is_ram = False
				if int(_bank, 16) > 0:
					address_string = 'rom{}::{}'.format(int(_bank, 16), _addr)
				else:
					address_string = _addr
			
			rom_address = toAddr(address_string)
			
			if is_ram:
				createLabel(rom_address, sym, False)
				print("Created label {} at address {}".format(sym, address_string))
			else:
				func = functionManager.getFunctionAt(rom_address)
				if func is not None:
					old_name = func.getName()
					func.setName(sym, USER_DEFINED)
					print("Renamed function {} to {} at address {}".format(old_name, sym, address_string))
				else:
					createLabel(rom_address, sym, False)
					print("Created label {} at address {}".format(sym, address_string))
