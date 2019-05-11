from django import forms
from django.forms import ModelForm, NumberInput, TextInput, Textarea

from api.models import Category, Lugar, Producto, Photo, Config, Mensaje

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ConfigForm(ModelForm):
	class Meta:
		model = Config
		fields = "__all__"
		exclude = ("user", "login_image")

class ConfigAdminForm(ModelForm):
	class Meta:
		model = Config
		fields = "__all__"
		exclude = ("user",)

class MensajeForm(ModelForm):
	class Meta:
		model = Mensaje
		fields = "__all__"

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
		fields = ("name",)
		# fields = ("nocontrol", "apellidop", "apellidom", "nombre", "edad", "sexo", "email", "celular", "telefono", "carrera", "semestre", "promedio", "curp", "lugarnac", "fechanac", "maestro1", "maestro2", "maestro3", "maestro4", "maestro1a", "maestro2a", "maestro3a", "maestro4a")

		labels = {
			# 'nombre' : 'Nombre(s)',			
		}

class LugarModelForm(ModelForm):

	class Meta:
		model = Lugar
		fields = "__all__"
		# fields = ("name", "category", "zone", "phone", "email", "description", "video", "mapa", "web", "photo")
		exclude = ("user", "clear_name", "nuevo", "sugerido")

		labels = {
			'name' : 'Nombre',
			'category' : 'Categoría',
			'zone' : 'Zona',
			'phone' : 'Teléfono',
			'email' : 'Email',
			'precio' : 'Precio promedio por persona',
			'description' : 'Descripción',
			'address' : 'Dirección',
			'photo' : 'Foto del lugar',
			'photoweb' : 'Foto de sitio web / promoción',
		}

	def __init__(self, *args, **kwargs):
		super(LugarModelForm, self).__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.objects.filter(tipo='lugar')
		self.fields['zone'].required = True

class ProductoModelForm(ModelForm):

	class Meta:
		model = Producto
		fields = ("name", "price", "category", "lugar", "description", "photo")
		# fields = ("nocontrol", "apellidop", "apellidom", "nombre", "edad", "sexo", "email", "celular", "telefono", "carrera", "semestre", "promedio", "curp", "lugarnac", "fechanac", "maestro1", "maestro2", "maestro3", "maestro4", "maestro1a", "maestro2a", "maestro3a", "maestro4a")

		labels = {
			'name' : 'Nombre',			
			'description' : 'Descripción',			
			'price' : 'Precio',			
			'category' : 'Categoria',			
			'lugar' : 'Lugar',			
		}
	
	def __init__(self, user=None, *args, **kwargs):
		super(ProductoModelForm, self).__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.objects.filter(tipo='producto').filter(user=user)
		if user:
			self.fields['category'].queryset = Category.objects.filter(user=user)
			self.fields['lugar'].queryset = Lugar.objects.filter(user=user)

class PhotoModelForm(ModelForm):

	class Meta:
		model = Photo
		fields = ("photo",)		
		labels = {
		}