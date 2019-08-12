from django.shortcuts import render,redirect,get_object_or_404
from .forms import HomeForm, CommentForm
from django.views.generic import ListView, DetailView,View
from .models import Post,Friend,Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.defaults import server_error

class HomeView(View):
    template_name = 'home/post_create.html'

    def get(self, request):
        form = HomeForm()
        posts = Post.objects.all().order_by('-created_on')
        users = User.objects.exclude(id=request.user.id)
        #Friend.objects.get(current_user=request.user)
        friend,created = Friend.objects.get_or_create(current_user=request.user)
        friends = friend.users.all()
        return render(request, self.template_name, {'form': form,'posts':posts,'users':users,'friends':friends})

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            print(request.user)
            post.save()

            text = form.cleaned_data['post']
            form = HomeForm()
            return redirect('home:home')

        args = {'form': form}
        return render(request, self.template_name, args)


def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home:home')


@login_required
def add_comment_to_post(request, pk):
   post= get_object_or_404(Post, pk=pk)
   #comments = Comment.objects.all()
   datas = Post.objects.order_by('-created_on')
   if request.method == 'POST':
       form = CommentForm(request.POST)
       if form.is_valid():
          comment = form.save(commit=False)
          comment.post= post
          comment.user = request.user
          comment.save()
          return redirect('home:add_comment_to_post', pk=post.pk)
   else:
       form = CommentForm()
   return render(request, 'home/add_comment_to_post.html', {'form':form,'post':post,'datas':datas})



@login_required
def delete_my_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    print(comment.user)
    print(request.user)
    if comment.user == request.user:
        comment.delete()
    else:
        raise Http404
    return redirect('home:add_comment_to_post', pk=comment.post.pk)

def deletemypost(request,id):
    dlpost=Post.objects.get(id=id)
    dlpost.delete()
    return redirect('/')
