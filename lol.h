/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lol.h                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaguillo <jaguillo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2015/09/16 16:15:39 by jaguillo          #+#    #+#             */
/*   Updated: 2015/09/16 16:30:39 by jaguillo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef LOL_H
# define LOL_H

/*
** [end]
** [enum] test
** char const		*str;
** char				c;
** A("a", 'a'),
** B("b", 'b'),
** C("c", 'c')
*/

/*
** [end]
*/

struct			s_evalue_shader_t
{
	char const		*name;
	int				gl_name;
};

typedef struct s_evalue_shader_t const*		t_shader_t;

struct			s_enum_shader_t
{
	t_shader_t			all;
	t_shader_t			vert;
	t_shader_t			frag;
	int					length;
	t_shader_t const	*values;
};

extern struct s_enum_shader_t const		g_shader_t;

#endif
