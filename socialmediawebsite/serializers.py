from rest_framework import serializers


class PostImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)


class PostSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    datetime = serializers.DateTimeField(required=True)
    author = serializers.CharField(required=True)

    images = PostImageSerializer(many=True)

