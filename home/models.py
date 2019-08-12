from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    users=models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True,on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_user):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_user)

    @classmethod
    def lose_friend(cls, current_user, new_user):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_user)