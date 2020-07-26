from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render,redirect
from .models import Post, userProfile, Like, Following, Comments
from django.contrib import messages
from django.contrib.auth.models import User
import json
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from .forms import CommentForm
# Create your views here.
def userhome(request):
    #fetching data from database
    user = Following.objects.get(user = request.user)

    followed_users = [i for i in user.followed.all()]
    followed_users.append(request.user)

    posts = Post.objects.filter(user__in = followed_users).order_by('-pk')
    liked_post = [i for i in posts if Like.objects.filter(post=i, user=request.user)]
    data = {
        'posts':posts,
        "liked_post":liked_post,
    }
    return render(request, 'userpage/postfield.html',data)

def post(request):
    if request.method=="POST":
        caption_ = request.POST.get('caption','')
        user_ = request.user
        image_ = request.FILES['images']
        post_obj = Post(user = user_, image = image_, caption = caption_)
        post_obj.save()
        messages.success(request,'finished your post')
        return redirect('/user')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('/user')

def delpost(request, postId):
    post_ = Post.objects.filter(pk=postId)
    image_path = post_[0].image.url
    post_.delete()
    messages.info(request, 'Post Deleted')
    return redirect('/user')

def Profile(request, username):
    user = User.objects.filter(username = username)
    if request.method=='POST':
        user_bio = request.POST.get('bio','')
        user_img = request.FILES['prof_image']
        web_url = request.POST.get('connect', '')
        v = userProfile.objects.get(user=request.user)
        v.bio = user_bio
        v.userImage = user_img
        v.connections = web_url
        v.save()
    if user:
        profile = userProfile.objects.get(user=user[0])
        post = getPost(user[0]),
        bio_ = profile.bio
        connection_ = profile.connections
        followers = profile.followers
        following = profile.following
        user_img = profile.userImage

        is_follow = Following.objects.filter(user = request.user, followed = user[0])

        following_obj = Following.objects.get(user = user[0])
        followers, following = following_obj.follower.count(), following_obj.followed.count()
        data = {
            'username':user[0],
            'bio':bio_,
            'con':connection_,
            'followers':followers,
            'following':following,
            'user_img' : user_img,
            'posts': post,
            'connection': is_follow,
        }
    else:
        return HttpResponse('No such user!')
    return render(request, 'userpage/userprofile.html', {'data':data})

def getPost(user):
    post_obj = Post.objects.filter(user=user)
    imagelist = [post_obj[i:i+3] for i in range(0, len(post_obj),3)]
    return imagelist

def likepost(request):
    post_id = request.GET.get("likeid","")
    post = Post.objects.get(pk=post_id)
    user = request.user
    like = Like.objects.filter(post=post, user=user)
    liked = False

    if like:
        Like.dislike(Like, post, user)
    else:
        liked = True
        Like.like(Like,post,user)
    
    resp = {
        "liked":liked
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type = "application/json")

def comment(request,PostId):
    user = request.user
    post = Post.objects.get(pk = PostId)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_ = Comments(
            post = post,
            user = user,
            comment = form.cleaned_data["body"]
            )
            comment_.save()
    comments = Comments.objects.filter(post=post)
    context = {
           'user':user,
           'comment':comments,
           'post':post,
           'form' : form,
       }

    return render(request, 'userpage/comments.html',{'context':context})

def follow(request, username):
    main_user = request.user
    to_follow = User.objects.get(username = username)
    
    following = Following.objects.filter(user = main_user, followed = to_follow)
    if following:
        is_following = True
    else:
        is_following = False
    
    if is_following:
        Following.unFollow(main_user, to_follow)
        is_following = False
    else:
        Following.follow(main_user, to_follow)
        is_following = True
    
    resp = {
        "following" : is_following
    }

    response = json.dumps(resp)
    return HttpResponse(response, content_type = "application/json")

class search_user(ListView):
    model = User
    template_name = "userpage/search.html"
    paginate_by = 10
    def get_queryset(self):
        username = self.request.GET.get("username", "")
        queryset = User.objects.filter(username__icontains = username)
        return queryset