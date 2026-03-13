from rest_framework import serializers
from GDMFX.models import Leads, Vehicles, Contract, Meets, Sales, BlogPost, PostImage, PostComment

class LeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = '__all__'

class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class MeetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meets
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'