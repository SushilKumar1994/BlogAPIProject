from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


from . models import Post,Comment,UserProfile,User

# Register your models here.

@admin.register(User)
class UserAdmin1(DjangoUserAdmin):
    list_display = ("id",'email', 'is_staff','date_joined','is_active')
    # here in fieldsets we add the fields which users can see in admin panel
    fieldsets = (
        (None, {'fields': ('email', 'password','is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_staff','is_active')}
        ),
    )
    ordering = ('email',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'first_name',
        'last_name',
        'username'
    )
    list_filter = (
        'username',
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'title',
        'body',
        'created',
        'updated',
        'status'
    )
    list_filter = (
        'created',
        'updated'
    )
    readonly_fields=('created','updated') 
    
    search_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'content',
        'timestamp',
    )
    readonly_fields=('timestamp',) 
