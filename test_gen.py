#!/usr/bin/python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_gen.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/09/15 22:41:07 by juloo             #+#    #+#              #
#    Updated: 2015/09/16 16:48:58 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sys import argv, stdout
import enum_generator, utils

#

INITIAL_CODE = """#
# Generated script
#

from sys import stdout, stderr

#
#
#

# Write to the current output
def out(s):
	_output.write(s)

# Write to stderr
def err(s):
	stderr.write(s)

#
# Internal functions
#
_output = None

# Close current output
def _close_output():
	# global _output
	# if _output != None:
	# 	_output.close()
	# 	_output = None
	pass

# Change current output
def _set_output(file_name):
	global _output
	# try:
	# 	f = open(file_name, "w")
	# except:
	# 	err("Error: Cannot open %s\\n" % (file_name))
	# 	exit(1)
	# _close_output()
	# _output = f
	_output = stdout

#
#
#

"""

END_CODE = """
_close_output()
"""

COMMENT_START = "/*"
COMMENT_END = "*/"

MARKUP_END = "[end]"

#

SET_OUT_CODE = "_set_output(\"%s\")\n"

#

#
# Generators
#

def _code_generator(code):
	for c in code:
		utils.out_code(c)

#
GENERATORS = [
	{"markup": "[code]",		"generator": _code_generator},
	{"markup": "[enum]",		"generator": enum_generator.enum},
	{"markup": "[enum-def]",	"generator": enum_generator.enum_def}
]

#
# Parser
#

# Trim comment line start
def _trim_comment(comment, (markup_index, markup_line), markup_length):
	comment[markup_line] = comment[markup_line][markup_index + markup_length:]
	if comment[markup_line].startswith(' '):
		comment[markup_line] = comment[markup_line][1:]
	for i in range(markup_line + 1, len(comment)):
		comment[i] = comment[i][markup_index:]
	return comment

#
def _exec_comment_util(f, (l, comment), (markup_index, markup_line), generator):
	while True:
		for c in comment:
			utils.out_text(c)
		comment = _trim_comment(comment, (markup_index, markup_line), len(generator['markup']))
		generator['generator'](comment[markup_line:])
		try:
			while True:
				start_index = l.find(COMMENT_START)
				if start_index >= 0:
					l, comment = _parse_comment(f, l[start_index:])
					markup_line = 0
					for c in comment:
						if c.find(MARKUP_END) >= 0:
							return _exec_comment(f, (l, comment), markup_line)
						markup_line += 1
					break
				l = f.next()
		except:
			pass
		markup_line = 0
	return l

# Search code in a comment and exec it
# Return the string after the comments
def _exec_comment(f, (l, comment), start_line):
	for generator in GENERATORS:
		markup_line = start_line
		for i in range(start_line, len(comment)):
			markup_index = comment[i].find(generator['markup'])
			if markup_index >= 0:
				return _exec_comment_util(f, (l, comment), (markup_index, markup_line), generator)
			markup_line += 1
	for c in comment:
		utils.out_text(c)
	return l

# Parse a comment
# Return ("after comment", ["comment"])
def _parse_comment(f, l):
	comment = []
	try:
		while True:
			end_index = l.find(COMMENT_END)
			if end_index >= 0:
				c = end_index + len(COMMENT_END)
				if l[c] == '\n':
					c += 1
				comment.append(l[:c])
				return (l[c:], comment)
			comment.append(l)
			l = f.next()
	except:
		pass
	return ("", comment)

# Start parsing and generating
def start_gen(file_name):
	try:
		f = open(file_name, "r")
	except:
		utils.error("Cannot open %s" % file_name)
	utils.out_code(SET_OUT_CODE % file_name)
	for l in f:
		start_index = l.find(COMMENT_START)
		if start_index >= 0:
			if start_index > 0:
				utils.out_text(l[:start_index])
			l = _exec_comment(f, _parse_comment(f, l[start_index:]), 0)
		utils.out_text(l)

#
# main
#

utils.out_code(INITIAL_CODE)

if len(argv) <= 1:
	utils.error("Not enougth argument")

for i in range(1, len(argv)):
	start_gen(argv[i])

utils.out_code(END_CODE)
stdout.flush()
