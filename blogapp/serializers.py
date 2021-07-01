from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from blogapp.models import *


from django.contrib.auth.hashers import check_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        try:
            token = super().get_token(user)
        except Exception as e:
            print('login error=',str(e))
            # Add custom claims
            # token['name'] = user.first_name
        return token
            
    def validate(self, attrs):
        print('attrs=',list(attrs.values()))
        attr=list(attrs.values())
        try:
            check_user=User.objects.get(email=attr[0])
            print('email',check_user,check_user.password)
            
        except:
            raise serializers.ValidationError("No User exists with this email")
        
        if not check_user.check_password(attr[1]):
            raise serializers.ValidationError("Incorrect password")

        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        try:
            userprofile_obj=UserProfile.objects.get(user=self.user)
        except:
            raise serializers.ValidationError("No User exists with the given credentials")
        
        data.update({'user':userprofile_obj.id})        
        data.update({'first_name':userprofile_obj.first_name})
        data.update({'last_name':userprofile_obj.last_name})
        data.update({'email':userprofile_obj.user.email})
        data.update({'password':userprofile_obj.user.password})
        
        return data



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all(),
            message="This email already exists"
            )]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
        email= validated_data['email'],
        password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = '__all__'

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','email')


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
 
    class Meta:
        model=UserProfile
        fields=('id','user','first_name','last_name','username')
        # exclude = ('created_date','modified_date','created_user','modified_user')

    def get_user(self,obj):
        user_qs=User.objects.filter(email=obj.user.email)
        user_data=UserDataSerializer(user_qs,many=True).data
        return user_data

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile 
        fields="__all__"

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['id','title','body','status']


class PostListSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields=['id','user','title','body','created','updated']

    def get_user(self,obj):
        return obj.user.email
#

class CommentListtSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Comment
        fields=(
                'id',
                'user',
                'content',
                'timestamp',
                )

class PostDetailSerializer(serializers.ModelSerializer):
    comments=CommentListtSerializer(many=True)
    class Meta:
        model=Post
        fields=['id','user','title','body','created','updated','comments']
        

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('id','post','content')

class CommentListSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Comment
        fields=(
                'id',
                'user',
                'post', 
                'content',
                'timestamp',
                )

class CommentUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Comment
        fields=('id','content','timestamp')





