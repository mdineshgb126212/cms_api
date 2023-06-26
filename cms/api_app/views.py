from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api_app.models import User, Post, Like
from django.contrib.auth.decorators import login_required
from django.db.models import Count




def create_user(request):
    name = request.POST['name of the user']
    email = request.POST['email of the user']
    password = request.POST['password of the user']

    user = User.objects.create(name=name , email=email, password=password)
    data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,

    }
    return JsonResponse(data)

def create_post(request):
    title = request.POST['title']
    description = request.POST['description']
    content = request.POST['content']
    owner_id = request.POST['owner_id']

    post = Post.objects.create(title=title, description=description, content=content, owner_id=owner_id)
    data = {
        'id': post.id,
        'title': post.title,
        'description': post.description,
    }
    return JsonResponse(data)

def create_like(request):
    post_idn = request.POST['post_id']
    user_idn = request.POST['user_id']

    like = Like.objects.create(post_id=post_idn, user_id=user_idn)
    data = {
        'id': like.id,
        'post_id': like.post_id,
        'user_id': like.user_id
    }
    return JsonResponse(data)

  # Read API

def get_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    data = {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }
    return JsonResponse(data)

def get_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not post.is_public and(not request.user.is_authenticated or request.user != post.owner):
      return JsonResponse({'error': 'Unauthorized'}, status=403)
    post_data = Post.objects.filter(id=post_id).annotate(like_count=Count('like')).values('id','title','description','like_count','content','creation_date').first()
    if post_data is None:
      return JsonResponse({'error':'Post Not Found'}, status=404)
    return JsonResponse(post_data)
    like_count = Like.objects.filter(post=post.count())
    data = {
        'id': post_id,
        'title': post.title,
        'description': post.description,
        'like_count': like_count,
    }
    return JsonResponse(data)
def get_like(request, like_id):
    like = get_object_or_404(Like, id=like_id)

    data = {
        'id': like_id,
        'post_id':like.post_id,
        'user_id':like.user_id,
    }
    return JsonResponse(data)
# Update API
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.save()
    data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,

    }
    return JsonResponse(data)

@login_required
def update_post(request, post_id):
    post = get_object_or_404(User, id=post_id)

    if request.user != post.owner:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    post.title = request.POST['title']
    post.description = request.POST['description']
    post.content = request.POST['content']
    post.save()
    data={
        'id': post.id,
        'title': post.title,
        'description': post.description,
    }
    return JsonResponse(data)

def update_like(request, like_id):
    like = get_object_or_404(Like, id=like_id)

    like.post_id = request.POST['post_id']
    like.user_id = request.POST['user_id']
    like.save()
    data = {
        'id': like.id,
        'post_id': like.post_id,
        'user_id': like.user_id,
    }
    return JsonResponse(data)

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    data = {
        'message': 'User deleted successfully'
    }
    return JsonResponse(data)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.owner:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    post.delete()
    data = {
        'message': 'Post deleted successfully'
    }
    return JsonResponse(data)

def delete_like(request, like_id):
    like = get_object_or_404(Like, id = like_id)
    like.delete()
    data = {
        'message': 'Like deleted successfully'
    }
    return JsonResponse(data)

def get_all_posts(request):
    posts = Post.objects.annoatate(like_count=Count('like'))
    data = []
    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'like_count': post.like_count,
        }
        data.append(post_data)
    return JsonResponse(data, safe=False)


