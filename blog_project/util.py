import string, random
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.title)
	Klass = instance.__class__
	# max_length = Klass._meta.get_field('slug').max_length
	# slug = slug[:max_length]
	qs_exists = Klass.objects.filter(slug=slug).exists()
	
	if qs_exists:
		random_str = random_string_generator(size=4)
		# slug = slug[:max_length-5]
		new_slug = f"{slug}-{random_str}"
		return unique_slug_generator(instance, new_slug=new_slug)
	return slug
