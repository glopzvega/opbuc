from django import forms
from django.forms import ModelForm, NumberInput, TextInput, Textarea

from api.models import Category, Lugar, Producto, Photo

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
	# first_name = forms.CharField(max_length=30, required=False, help_text='Opcional.')
	# last_name = forms.CharField(max_length=30, required=False, help_text='Opcional.')
	email = forms.EmailField(max_length=255, help_text='Requerido. Proporciona una dirección de email válida.')

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', )
	
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuario"
		self.fields['password1'].label = "Contraseña"
		self.fields['password2'].label = "Repetir Contraseña"
		self.fields['password1'].help_text = "<ul><li>Tu contraseña no debe ser muy similar a tu otra información personal</li><li>Tu contraseña debe contener al menos 8 caracteres</li><li>Tu contraseña no puede ser una palabra común, por ej. 123456, minombre.</li><li>Tu contraseña no puede ser completamente numérica.</li></ul>"
		self.fields['password2'].help_text= "Introduce la misma contraseña de antes para verificarla"
		self.fields['username'].help_text= "Requerido. 150 caracteres o menos. Letras, digitos y @/./+/-/_ solamente."



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
		# fields = "__all__"
		fields = ("name", "category", "zone", "phone", "email", "description")
		# exclude = ("photo",)


		labels = {
			'name' : 'Nombre',
			'category' : 'Categoría',
			'zone' : 'Zona',
			'phone' : 'Teléfono',
			'email' : 'Email',
			'description' : 'Descripción',
		}

class ProductoModelForm(ModelForm):

	class Meta:
		model = Producto
		fields = ("name", "description", "price", "category", "lugar")
		# fields = ("nocontrol", "apellidop", "apellidom", "nombre", "edad", "sexo", "email", "celular", "telefono", "carrera", "semestre", "promedio", "curp", "lugarnac", "fechanac", "maestro1", "maestro2", "maestro3", "maestro4", "maestro1a", "maestro2a", "maestro3a", "maestro4a")

		labels = {
			# 'nombre' : 'Nombre(s)',			
		}

class PhotoModelForm(ModelForm):

	class Meta:
		model = Photo
		fields = ("photo",)		
		labels = {
		}