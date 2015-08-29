from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class Provincia(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=30)
    provincia = models.ForeignKey(Provincia)

    def __unicode__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    clave = models.CharField(max_length=20)

    def __unicode__(self):
        return self.nombre


class UserManager(BaseUserManager, models.Manager):
    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
        username = self.normalize_email(username)
        user = self.model(username=username, is_active=True, is_staff=is_staff,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password, False, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(unique=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10,unique=True)
    telefono = models.CharField(max_length=10)
    fecha_nac = models.DateField()
    ciudad = models.ForeignKey(Ciudad)
    rol = models.ForeignKey(Rol)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    object = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['']

    def get_short_name(self):
        return self.nombres



class Categoria(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    precio = models.FloatField()
    cantidad = models.CharField(max_length=10)
    categoria = models.ForeignKey(Categoria)

    def __unicode__(self):
        return self.nombre


class Foto(models.Model):
    imagen = models.ImageField(upload_to="fotos", default='/media/default.png')
    producto = models.ForeignKey(Producto)

class Pedido(models.Model):
    fecha_ini = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=10)
    usuario = models.ForeignKey(User)

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido)
    producto = models.ForeignKey(Producto)
    cantidad = models.IntegerField()

class Publicidad(models.Model):
    descripcion = models.CharField(max_length=100)
    imagen = models.CharField(max_length=300)
    usuario = models.ForeignKey(User)


