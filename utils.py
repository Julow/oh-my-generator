# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utils.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/09/16 16:34:09 by jaguillo          #+#    #+#              #
#    Updated: 2015/09/16 16:55:02 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sys import stdout

TEXT_START = "\nout(\"\"\""
TEXT_END = "\"\"\")\n\n"

#

in_text = False

# Output text
def out_text(text):
	global in_text
	if len(text) > 0:
		if not in_text:
			in_text = True
			stdout.write(TEXT_START)
		stdout.write(text.replace("\\", "\\\\"))

# Output code
def out_code(code):
	global in_text
	if in_text:
		in_text = False
		stdout.write(TEXT_END)
	stdout.write(code)

# Print an error and exit
def error(err):
	out_code("\n\033[31m[///ERROR///]\033[0m %s\n" % err)
	exit(1)
