# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    omg_enum.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/09/16 16:32:50 by jaguillo          #+#    #+#              #
#    Updated: 2015/09/21 09:02:19 by jaguillo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from collections import OrderedDict
import utils, re

ENUM_CODE = """
struct			s_evalue_%(name)s
{
%(fields)s};

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

ENUM_OPT_MACRO_LEN = ("length-macro", "# define %(macro)s		%(length)s\n\n")

ENUM_DEF_PARAMS = "	&(struct s_evalue_%(enum)s){%(params)s},\n"

ENUM_PARAM_REG = re.compile('^([a-zA-Z0-9_]+)\((.*)\),?$')
ENUM_OPTION_REG = re.compile('([a-zA-Z0-9_-]+)(?:\((.*)\))?')

# {"<enum name>": {"fields": [], "values": {"<name>": ["<params>"]}, "options": {"opt": "args"}}
enums = {}

# Process options
def _process_options(enum):
	pass

# Parse an enum
def _parse_enum(code, options):
	fields = []
	values = OrderedDict()
	in_structs = True
	param_id = 0
	for l in code:
		if in_structs:
			if l.endswith(";\n"):
				fields.append(l)
			else:
				in_structs = False
		if not in_structs:
			m = ENUM_PARAM_REG.match(l)
			if m != None:
				param_name = m.group(1)
				values[param_name] = m.group(2).replace(
					"?id?", str(param_id)).replace(
					"?name?", param_name)
				param_id += 1
	enum = {"fields": fields, "values": values, "options": options}
	_process_options(enum)
	return enum

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
	if ENUM_OPT_MACRO_LEN[0] in enum["options"]:
		utils.out_text(ENUM_OPT_MACRO_LEN[1] % {
			"macro": enum["options"][ENUM_OPT_MACRO_LEN[0]],
			"length": len(enum["values"])
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
	opt = {}
	name = None
	for m in ENUM_OPTION_REG.finditer(code[0][:-1]):
		if name == None:
			name = m.group(1)
			opt["name"] = name
		else:
			opt[m.group(1)] = m.group(2)
	if name == None:
		utils.error("?enum require an enum name")
	enums[name] = _parse_enum(code[1:], opt)
	_print_enum(name, enums[name])

#
# Initialize a declared enum
#
def enum_def(code):
	if len(code) == 0 or len(code[0]) <= 1:
		utils.error("?enum-def need an argument (enum name)")
	name = code[0][:-1]
	if not name in enums:
		utils.error("?enum-def unknown enum: %s" % name)
	_print_def_enum(name, enums[name])
