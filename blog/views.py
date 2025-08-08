
from django.shortcuts import render
from .models import Post
from django.views.generic import ListView
from .froms import CommentForm
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse


class StartingPageView(ListView):
  template_name = 'blog/index.html'
  model = Post
  ordering = ['-date']
  context_object_name = 'posts'

  def get_queryset(self):
    query =  super().get_queryset()
    data = query[:3]
    return data
  
  

class AllPostView(ListView):
  template_name = "blog/all-posts.html"
  model = Post
  context_object_name = 'posts'
  ordering = ["-date"]


class PostDetail(View):

  def is_stored_post(self, request, post_id):
    stored_post = request.session.get("stored_posts")

    if stored_post is not None:
      is_saved_for_later = post_id in stored_post
    else:
      is_saved_for_later = False
    return is_saved_for_later

  def get(self, request, slug):
    post = Post.objects.get(slug=slug)
    context = {
      'post':post,
      'post_tags':post.tags.all(),
      'comment_form':CommentForm(),
      'comments':post.comments.all(),
      'is_saved_for_later':self.is_stored_post(request, post.id)
    }
    return render(request, "blog/post-detail.html", context)

  def post(self, request,slug):
    post = Post.objects.get(slug=slug)
    form = CommentForm(request.POST)

    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = post
      comment.save()
      return HttpResponseRedirect(reverse('post-detail-page',args=[slug]))
    
    
    context = {
      'post':post,
      'post_tags':post.tags.all(),
      'comment_form':form,
      'comments':post.comments.all(),
      'is_saved_for_later':self.is_stored_post(request, post.id)
    }
    return render(request, "blog/post-detail.html", context)


class LoadLaterView(View):
  
  def get(self, request):
    stored_posts = request.session.get('stored_posts')

    context = {}
    if stored_posts is None or len(stored_posts) == 0:
      context['posts'] = []
      context['has_post'] = False
    else:
      posts = Post.objects.filter(id__in=stored_posts)
      context['posts'] = posts
      context['has_post'] = True

    return render(request, 'blog/read-later.html', context)


  def post(self, request):
    print('called')
    stored_posts = request.session.get('stored_posts')
    
    if stored_posts is None:
      stored_posts = []

    post_id = int(request.POST['post_id'])

    if post_id not in stored_posts:
      stored_posts.append(post_id)
    else:
      stored_posts.remove(post_id)

    request.session['stored_posts'] = stored_posts
      
    return HttpResponseRedirect("/")