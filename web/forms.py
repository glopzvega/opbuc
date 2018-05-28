from django import forms
from django.forms import ModelForm, NumberInput, TextInput, Textarea

from api.models import Category, Lugar, Producto

class CategoriaModelForm(ModelForm):

	class Meta:
		model = Category
		fields = "__all__"
		# fields = ("nocontrol", "apellidop", "apellidom", "nombre", "edad", "sexo", "email", "celular", "telefono", "carrera", "semestre", "promedio", "curp", "lugarnac", "fechanac", "maestro1", "maestro2", "maestro3", "maestro4", "maestro1a", "maestro2a", "maestro3a", "maestro4a")

		labels = {
			# 'nombre' : 'Nombre(s)',			
		}

class LugarModelForm(ModelForm):

	class Meta:
		model = Lugar
		fields = "__all__"
		# fields = ("nocontrol", "apellidop", "apellidom", "nombre", "edad", "sexo", "email", "celular", "telefono", "carrera", "semestre", "promedio", "curp", "lugarnac", "fechanac", "maestro1", "maestro2", "maestro3", "maestro4", "maestro1a", "maestro2a", "maestro3a", "maestro4a")

		labels = {
			# 'nombre' : 'Nombre(s)',			
		}

class ProductoModelForm(ModelForm):

	class Meta:
		model = Producto
		fields = "__all__"
		# fields = ("nocontrol", "apellidop", "apellidom", "nombre", "edad", "sexo", "email", "celular", "telefono", "carrera", "semestre", "promedio", "curp", "lugarnac", "fechanac", "maestro1", "maestro2", "maestro3", "maestro4", "maestro1a", "maestro2a", "maestro3a", "maestro4a")

		labels = {
			# 'nombre' : 'Nombre(s)',			
		}