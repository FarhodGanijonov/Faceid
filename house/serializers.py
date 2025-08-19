from rest_framework import serializers
from .models import House, House_image, Region, District, Comment
from django.shortcuts import get_object_or_404


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'districts']


class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = House_image
        fields = ['id', 'image']


class HouseSerializer(serializers.ModelSerializer):
    images = HouseImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    is_saved = serializers.SerializerMethodField()


    class Meta:
        model = House
        fields = [
            'id', 'title', 'price', 'region', 'district', 'room_count', 'description',
            'views_count', 'images', 'uploaded_images', 'is_saved',
        ]

    def get_is_saved(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.saved_by.filter(id=user.id).exists()
        return False


    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        house = House.objects.create(**validated_data)

        for image in uploaded_images:
            House_image.objects.create(house=house, image=image)

        return house


class CommentSerializer(serializers.ModelSerializer):
    house_id = serializers.IntegerField(write_only=True)
    house = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'house_id', 'house', 'user', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def get_house(self, obj):
        if obj.house:
            return {"id": obj.house.id, "title": obj.house.title}
        return None

    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "fullname": obj.user.fullname,
                "phone": getattr(obj.user, "phone", None)
            }
        return None

    def validate_house_id(self, value):
        if not House.objects.filter(id=value).exists():
            raise serializers.ValidationError("Bunday uy mavjud emas.")
        return value

    def create(self, validated_data):
        house_id = validated_data.pop('house_id')
        house = get_object_or_404(House, id=house_id)
        comment = Comment.objects.create(**validated_data, house=house)
        return comment