from rest_framework import serializers


class PostImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)


class PostSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    datetime = serializers.DateTimeField(required=True)
    author = serializers.CharField(required=True)

    images = PostImageSerializer(many=True)

    like_status = serializers.SerializerMethodField()
    dislike_status = serializers.SerializerMethodField()

    def get_like_status(self, post):
        request = self.context.get('request', None)
        current_user = request.user

        like_status = False
        if current_user in post.likes.all():
            like_status = True
        return like_status

    def get_dislike_status(self, post):
        request = self.context.get('request', None)
        current_user = request.user

        dislike_status = False
        if current_user in post.dislikes.all():
            dislike_status = True
        return dislike_status
