# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    omg_enum.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/09/16 16:32:50 by jaguillo          #+#    #+#              #
#    Updated: 2015/09/17 08:12:27 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import utils
import re

ENUM_CODE = """
struct			s_evalue_%(name)s
{
%(fields)s
};

typedef struct s_evalue_%(name)s const*		t_%(name)s;

struct			s_enum_%(name)s
{
%(values)s	int					length;
	t_%(name)s const	*values;
};

extern struct s_enum_%(name)s const		g_%(name)s;

"""

ENUM_DEF_CODE = """
struct s_enum_%(name)s const	g_%(name)s = {
%(params)s	%(size)d,
	(t_%(name)s const*)&g_%(name)s
};

"""

ENUM_VALUE = "	%(value)s"
ENUM_FIELD = "	t_%(enum)s			%(name)s;\n"

ENUM_DEF_PARAMS = "	&(struct s_evalue_%(enum)s){%(params)s},\n"

ENUM_PARAM_REG = re.compile('^([a-zA-Z0-9]+)\((.*)\),?$')

# {"<enum name>": {"fields": [], "values": {"<name>": ["<params>"]}}}
enums = {}

# Parse an enum
def _parse_enum(code):
	fields = []
	values = {}
	in_structs = True
	for i in range(1, len(code)):
		if in_structs:
			if code[i].endswith(";\n"):
				fields.append(code[i])
			else:
				in_structs = False
		if not in_structs:
			m = ENUM_PARAM_REG.match(code[i])
			if m != None:
				values[m.group(1)] = m.group(2)
	return {"fields": fields, "values": values}

# Print an enum declaration
def _print_enum(name, enum):
	fields = ""
	for s in enum["fields"]:
		fields += ENUM_VALUE % {"value": s}
	values = ""
	for v in enum["values"]:
		values += ENUM_FIELD % {
			"enum": name,
			"name": v
		}
	utils.out_text(ENUM_CODE % {
		"name": name,
		"fields": fields,
		"values": values
	})

# Print an enum def
def _print_def_enum(name, enum):
	params = ""
	for v in enum["values"]:
		params += ENUM_DEF_PARAMS % {
			"enum": name,
			"params": enum["values"][v]
		}
	utils.out_text(ENUM_DEF_CODE % {
		"name": name,
		"params": params,
		"size": len(enum["values"])
	})

#
# Declare an enum
#
def enum(code):
	global enums
	if len(code) == 0 or len(code[0]) <= 1:
		utils.error("[enum] need an argument (enum name)")
	name = code[0][:-1]
	enums[name] = _parse_enum(code)
	_print_enum(name, enums[name])

#
# Initialize a declared enum
#
def enum_def(code):
	if len(code) == 0 or len(code[0]) <= 1:
		utils.error("[enum-def] need an argument (enum name)")
	name = code[0][:-1]
	if not name in enums:
		utils.error("[enum-def] unknown enum: %s" % name)
	_print_def_enum(name, enums[name])
