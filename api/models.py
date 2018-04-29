from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

CATEGORIAS = [
	("lugar", "Lugar"),
	("producto", "Producto"),
]

class Zone(models.Model):
	name = models.CharField(max_length=255)
	photo = models.ImageField(blank=True, null=True)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=255)
	photo = models.ImageField(blank=True, null=True)
	tipo = models.CharField(max_length=255, choices=CATEGORIAS)

	def __str__(self):
		return self.name

class Lugar(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
	zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.SET_NULL)	

	def __str__(self):
		return self.name	

class Producto(models.Model):
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=20, decimal_places=2)
	description = models.TextField()
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
	photo = models.ImageField(blank=True, null=True)
	lugar = models.ForeignKey(Lugar, blank=True, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.name

class Comment(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateField(auto_now_add=True)
	comentario = models.TextField()
	lugar = models.ForeignKey(Lugar, blank=True, null=True, on_delete=models.CASCADE)	
	producto = models.ForeignKey(Producto, blank=True, null=True, on_delete=models.CASCADE)	
	like = models.BooleanField()
	
	class Meta:
		unique_together = ('usuario', 'lugar')

	def __str__(self):
		if self.lugar:
			return self.usuario.username + " " + self.lugar.name + " " + str(self.fecha)
		elif self.producto:
			return self.usuario.username + " " + self.producto.name + " " + str(self.fecha)
		else:
			return self.usuario.username + " " + str(self.fecha)


class Photo(models.Model):
	name = models.CharField(max_length=255)
	photo = models.ImageField()
	order = models.IntegerField()
	lugar_id = models.ForeignKey(Lugar, blank=True, null=True, related_name='photos', on_delete=models.CASCADE)
	producto_id = models.ForeignKey(Producto, blank=True, null=True, related_name='photos', on_delete=models.CASCADE)

	class Meta:
		# unique_together = ('lugar_id', 'order')
		ordering = ['order']

	def __str__(self):
		return '%i : %s' % (self.order, self.name)