from django.db import models

# Create your models here.

class Zone(models.Model):

	name = models.CharField(max_length=255)
	photo = models.ImageField(blank=True, null=True)

	def __str__(self):
		return self.name

class Category(models.Model):

	name = models.CharField(max_length=255)
	photo = models.ImageField(blank=True, null=True)

	def __str__(self):
		return self.name

class Lugar(models.Model):

	name = models.CharField(max_length=255)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
	zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.SET_NULL)	

	def __str__(self):
		return self.name	

class Photo(models.Model):
	name = models.CharField(max_length=255)
	photo = models.ImageField()
	order = models.IntegerField()
	lugar_id = models.ForeignKey(Lugar, related_name='photos', on_delete=models.CASCADE)

	class Meta:
		# unique_together = ('lugar_id', 'order')
		ordering = ['order']

	def __str__(self):
		return '%i : %s' % (self.order, self.name)