from django.shortcuts import (render, redirect,
                              get_object_or_404, render_to_response)
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template import RequestContext

from endless_pagination.decorators import page_template
from sorl.thumbnail import delete

from .forms import ProfileForm, PhotoForm
from article.models import Article, Likes


@login_required
def edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.bio = form.cleaned_data.get('bio')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')
            return redirect('/profile/edit')
    else:
        form = ProfileForm(instance=user, initial={
            'username': user.username,
            'location': user.profile.location,
            'bio': user.profile.bio
        })
    return render(request, 'edit/settings.html', {
        'form': form
        })


@login_required
def picture(request):
    return render(request, 'edit/picture.html')


@login_required
def upload_picture(request):
    user = request.user
    avatar = user.profile.avatar.name
    form = PhotoForm(request.POST, request.FILES, instance=user.profile)
    if avatar:
        delete(avatar)
    if form.is_valid():
        form.save()
        data = {'is_valid': True}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)


@page_template('article/articles_index_page.html')
def profile(request, username, template='edit/profile.html',
            extra_context=None):
    user = get_object_or_404(User, username=username)
    context = {
        'page_user': user,
        'article': Article.objects.filter(
                          author=user
                   ).order_by('-created_date')
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


@page_template('article/articles_index_page.html')
def liked(request, username, template='edit/profile.html',
          extra_context=None):
    user = get_object_or_404(User, username=username)
    liked = Likes.objects.filter(author=user).values('article')
    posts = Article.objects.filter(likes__article=liked).distinct()
    context = {
        'page_user': user,
        'article': posts
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))
