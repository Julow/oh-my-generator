# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    oh_my_generator.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juloo <juloo@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/09/15 22:41:07 by juloo             #+#    #+#              #
#    Updated: 2016/06/27 17:27:59 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sys import argv, stdout
import omg_enum, utils

#

INITIAL_CODE = """#
# Generated script
#

from sys import stdout, stderr
import tempfile, os, shutil

#
#
#

# Write to the current output
def out(s):
	global omg_output
	if omg_output != None:
		f, _, _ = omg_output
		f.write(s)

# Write to stderr
def err(s):
	stderr.write(s)

# Output a list
def out_list(lst, sep=", ", endl=",\\n", indent="\t", max_width=80, tab_size=4):
	i = 0
	nl = True
	for e in lst:
		e = str(e)
		i += len(sep) + len(e)
		if not nl and i >= max_width:
			nl = True
			out(endl)
		if nl:
			out(indent)
			out(e)
			i = len(indent.expandtabs(tab_size)) + len(e)
			nl = False
		else:
			out(sep)
			out(e)

#
# Internal functions
#
# (tmp_fd, tmp_file, dst_file)
omg_output = None

# Save and close current output
def omg_close_output():
	global omg_output
	if omg_output != None:
		f, tmp_file, dst_file = omg_output
		f.flush()
		os.fsync(f.fileno())
		f.close()
		os.unlink(dst_file)
		shutil.move(tmp_file, dst_file)
		omg_output = None

# Change current output
def omg_set_output(file_name):
	global omg_output
	omg_close_output()
	f, tmp_file = tempfile.mkstemp("", "omg_")
	omg_output = (os.fdopen(f, "w"), tmp_file, file_name)

#
#
#

"""

END_CODE = """
omg_close_output()
"""

COMMENT_START = "/*"
COMMENT_END = "*/"

MARKUP_END = "?end"

#

SET_OUT_CODE = "omg_set_output(\"%s\")\n"

#

#
# Generators
#

def _code_generator(code):
	for c in code:
		utils.out_code(c)

#
GENERATORS = [
	{"markup": "?omg",		"generator": _code_generator},
	{"markup": "?enum-def",	"generator": omg_enum.enum_def},
	{"markup": "?enum",		"generator": omg_enum.enum}
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
		if comment[i].startswith(MARKUP_END):
			return (comment[:i], True)
	return (comment, False)

#
def _exec_comment_util(f, (l, comment), (markup_index, markup_line), generator):
	while True:
		for c in comment:
			utils.out_text(c)
		comment, end = _trim_comment(comment, (markup_index, markup_line), len(generator['markup']))
		generator['generator'](comment[markup_line:])
		if end:
			return l
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
			utils.error("unclosed %s" % generator["markup"])
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
def main():
	utils.out_code(INITIAL_CODE)

	if len(argv) <= 1:
		utils.error("Not enougth argument")

	for i in range(1, len(argv)):
		start_gen(argv[i])

	utils.out_code(END_CODE)
	stdout.flush()
