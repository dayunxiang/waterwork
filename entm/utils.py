import random
import string

from django.utils.text import slugify
'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''

DONT_USE = ['create']
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_cid_generator(instance, new_cid=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_cid is not None:
        cid = new_cid
    else:
        cid = slugify(instance.pId)
    if cid in DONT_USE:
        new_cid = "{cid}_{randstr}".format(
                    cid=cid,
                    randstr=random_string_generator(size=4)
                )
        return unique_cid_generator(instance, new_cid=new_cid)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(cid=cid).exists()
    if qs_exists:
        new_cid = "{cid}_{randstr}".format(
                    cid=cid,
                    randstr=random_string_generator(size=4)
                )
        return unique_cid_generator(instance, new_cid=new_cid)
    return cid

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    if slug in DONT_USE:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug