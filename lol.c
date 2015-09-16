/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lol.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2015/09/16 13:26:16 by jaguillo          #+#    #+#             */
/*   Updated: 2015/09/16 17:25:25 by jaguillo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "lol.h"
#include <stdio.h>

#define MDR 5

/*
** laaaal
** laaaal
*/

#define LOL 0

/*
** [code]
** mdr = "mdr\n"
** out("xd\n")
*/

/*
** out(mdr)
*/

/*
** [code]
** [end]
*/

/*
** [end]
*/

/*
** [end]
** [enum-def] test
*/

/*
** [end]
*/

struct s_enum_shader_t const	g_shader_t = {
	&(struct s_evalue_shader_t){"all", 0},
	&(struct s_evalue_shader_t){"vert", 1},
	&(struct s_evalue_shader_t){"frag", 2},
	3,
	(t_shader_t const*)&g_shader_t
};

int				main(void)
{
	int				i;

	i = -1;
	while (++i < g_shader_t.length)
	{
		printf("%s %d\n",
			g_shader_t.values[i]->name, g_shader_t.values[i]->gl_name);
	}
	return (0);
}
