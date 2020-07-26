from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'user_image/post')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' '  + str(self.time.date)

class userProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userImage = models.ImageField(upload_to = 'user_image/profiles', default='user_image/default/default.jpg')
    bio = models.CharField(max_length = 100, blank=True)
    connections = models.CharField(max_length = 100, blank=True)
    followers = models.IntegerField(default = 0)
    following = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.user)

class Like(models.Model):
    user = models.ManyToManyField(User,related_name='liking_user')
    post = models.OneToOneField(Post,on_delete=models.CASCADE)

    def like(cls, post, liking_user):
        obj, create = cls.objects.get_or_create(post = post)
        obj.user.add(liking_user)

    def dislike(cls, post, disliking_user):
        obj, create = cls.objects.get_or_create(post = post)
        obj.user.remove(disliking_user)
    
    def __str__(self):
        return str(self.post)

class Following(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    followed = models.ManyToManyField(User, related_name = 'followed')
    follower = models.ManyToManyField(User, related_name = 'follower')
    
    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followed.add(another_account)
        print("followed")
    
    @classmethod
    def unFollow(cls, user , another_account):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.remove(another_account)
        print("unfollowed")

    def __str__(self):
        return str(self.user)

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "post")
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comment_user")
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return str(self.user)