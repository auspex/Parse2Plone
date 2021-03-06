###############################################################################
#                                                                             #
# Adds "slugify" support to parse2plone, which means that if a path like this #
# is discovered:                                                              #
#                                                                             #
#     /2000/01/01/foo/index.html                                              #
#                                                                             #
# And --slugify is called, then instead of creating /2000/01/01/foo/index.html#
# (in Plone), parse2plone will create:                                        #
#                                                                             #
#     /foo-20000101.html                                                      #
#                                                                             #
# thereby "slugifying" the content, if you will.                              #
#                                                                             #
###############################################################################

from re import compile

slug = compile('(\d\d\d\d)/(\d\d)/(\d\d)/(.+)/index.html')


def convert_path_to_slug(files, slug_map, base):
    """
    Returns a slug_map which is forward/reverse mapping of paths to slugified
    paths and vice versa. E.g.:

        slug_map{'forward': {'/var/www/html/2000/01/01/foo/index.html':
            '/var/www/html/foo-20000101.html'}}

        slug_map{'reverse': {'/var/www/html/foo-20000101.html':
            '/var/www/html/2000/01/01/foo/index.html'}}
    """

    for f in files[base]:
        result = slug.search(f)
        if result:
            groups = result.groups()
            slugfile = '%s-%s%s%s.html' % (groups[3], groups[0], groups[1],
                groups[2])
            slug_map['forward'][f] = slugfile
            slug_map['reverse'][slugfile] = f

    return slug_map
