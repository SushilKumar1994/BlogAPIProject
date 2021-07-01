from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.conf import settings

# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        #this is a private method and should not be used anywhere by anyone
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField( unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()    #custom model manager

    def __str__(self):
        return str(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=300,null=True,blank=True)
    last_name = models.CharField(max_length=300,null=True,blank=True)
    username = models.CharField(max_length = 15,null=True,blank=True,unique=True)

    def __str__(self):
        return str(self.user.email)

    
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")
class DraftedManager(models.Manager):
    def get_queryset(self):
        return super(DraftedManager,self).get_queryset().filter(status="draft")

class Post(models.Model):                                            # limit_choices_to={'is_staff':True}
    CATEGORY_CHOICE=(('draft','Draft'),('published','Published'))
  
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=100,blank="False")    #help_text=""
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=CATEGORY_CHOICE, default='draft')

    published = PublishedManager()  #Our Custom Model Manager 
    drafted=DraftedManager()
 
    class Meta:
        ordering = ['-id']          

    def __str__(self):
        return self.title
        
    @property
    def comments(self):    
        return self.comment_set.all()  
        
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)

    post=models.ForeignKey(Post,on_delete=models.CASCADE,default=1) #related_name="comments"

    content = models.TextField(max_length=160,blank="True")

    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.post.title) +"-" + str(self.user.id)
    

