from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

CATEGORIAS = [
	("lugar", "Lugar"),
	("producto", "Producto"),
]

ESTATUS = [
	('active', 'Activa'),
	('cancel', 'Bloqueada'),
]

class Mensaje(models.Model):
	mensaje = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	order = models.ForeignKey("Order", on_delete=models.CASCADE)

class Config(models.Model):
	facebook = models.CharField(max_length=255, blank=True, null=True)
	twitter = models.CharField(max_length=255, blank=True, null=True)
	instagram = models.CharField(max_length=255, blank=True, null=True)
	conekta_public = models.CharField(max_length=255, blank=True, null=True)
	conekta_private = models.CharField(max_length=255, blank=True, null=True)
	login_image = models.ImageField(blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Zone(models.Model):
	name = models.CharField(max_length=255)
	photo = models.ImageField(blank=True, null=True)

	def __str__(self):
		return self.name

class Category(models.Model):    
	name = models.CharField(max_length=255)
	photo = models.ImageField(blank=True, null=True)
	tipo = models.CharField(max_length=255, choices=CATEGORIAS)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=255, choices=ESTATUS, default="active")

	def __str__(self):
		return self.name

class Lugar(models.Model):
	name = models.CharField(max_length=255)
	clear_name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	lomejor = models.TextField(blank=True, null=True)
	accesibilidad = models.TextField(blank=True, null=True)
	servicios = models.TextField(blank=True, null=True)
	reglas = models.TextField(blank=True, null=True)
	promociones = models.FloatField(default=0)
	precio = models.FloatField(default=0)
	address = models.TextField(blank=True, null=True)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
	zone = models.ForeignKey(Zone, null=True, blank=True, on_delete=models.SET_NULL)	
	phone = models.IntegerField(blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	photo = models.ImageField(blank=True, null=True)
	photoweb = models.ImageField(blank=True, null=True)
	web = models.CharField(max_length=255, blank=True, null=True)
	video = models.TextField(blank=True, null=True)
	mapa = models.TextField(blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sugerido = models.BooleanField(default=False)
	nuevo = models.BooleanField(default=True)
	# conekta_public = models.CharField(max_length=255)
	# conekta_private = models.CharField(max_length=255)

	def __str__(self):
		return self.name	

class Producto(models.Model):
	name = models.CharField(max_length=255)
	price = models.FloatField(2)
	description = models.TextField()
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
	photo = models.ImageField(blank=True, null=True)
	lugar = models.ForeignKey(Lugar, blank=True, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.name

class Cobro(models.Model):
	STATES = [
		("draft", "Pendiente"),
		("done", "Realizado"),
	]
	name = models.CharField(max_length=255)
	lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
	fecha = models.DateField()
	state = models.CharField(max_length=255, choices=STATES, default="draft")
	total = models.FloatField()
	total_porcentaje = models.FloatField()
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	payment_info = models.TextField(default='')

	def __str__(self):
		return self.name

class Order(models.Model):
	STATES = [
		("draft", "Pendiente"),
		("done", "Realizado"),
	]
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=255)
	fecha_pedido = models.DateField()
	hora_pedido = models.TimeField()
	lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
	total = models.FloatField()
	state = models.CharField(max_length=255, choices=STATES, default="draft")
	invitados = models.IntegerField(default=1)
	cupon = models.FloatField(default=0)
	payment_info = models.TextField()
	status_entrega = models.CharField(max_length=255, default="draft", choices=[("draft", "Pendiente"), ("open", "En Proceso"), ("done", "Entregada"), ("cancel", "Cancelada")])
	payment_id = models.CharField(max_length=255, null=True, blank=True, default="")
	cobro_id = models.ForeignKey('Cobro', null=True, blank=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.name

class OrderLine(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateTimeField(auto_now_add=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	subtotal = models.FloatField()

class Comment(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateField(auto_now_add=True)
	comentario = models.TextField()
	lugar = models.ForeignKey(Lugar, blank=True, null=True, on_delete=models.CASCADE)	
	producto = models.ForeignKey(Producto, blank=True, null=True, on_delete=models.CASCADE)	
	puntuacion = models.IntegerField()
	# like = models.BooleanField()
	
	# class Meta:
	# 	unique_together = ('usuario', 'lugar')

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
	order = models.IntegerField(default=0)
	lugar_id = models.ForeignKey(Lugar, blank=True, null=True, related_name='photos', on_delete=models.CASCADE)
	producto_id = models.ForeignKey(Producto, blank=True, null=True, related_name='photos', on_delete=models.CASCADE)

	class Meta:
		# unique_together = ('lugar_id', 'order')
		ordering = ['order']

	def __str__(self):
		return '%i : %s' % (self.order, self.name)