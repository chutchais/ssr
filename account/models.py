from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
# Create your models here.
ACTIVE='A'
DEACTIVE='D'
STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DEACTIVE, 'Deactive'),
    )

class Company(models.Model):
	name = models.CharField(verbose_name ='Company',max_length=50)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('account:detail', kwargs={'slug':self.slug})


# Company Slug Hadeling#
def create_company_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Company.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count())
        return create_company_slug(instance, new_slug=new_slug)
    return slug

def pre_save_company_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_company_slug(instance)

pre_save.connect(pre_save_company_receiver, sender=Company)