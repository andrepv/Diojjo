from django.shortcuts import (render, redirect,
                              get_object_or_404, render_to_response)
from django.template import RequestContext
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.db.models import Count

from endless_pagination.decorators import page_template
from sorl.thumbnail import delete

from .forms import ArticleForm, ImageForm, Zone
from .models import Article, Images, Likes, Comment, PointOfInterest

@page_template('article/articles_index_page.html')
def articles(request, template='article/articles.html',
             extra_context=None):
    article = Article.objects.annotate(likes_count=Count('likes'))
    context = {
        'article': article.filter(
                   likes_count__gte=2
         ).order_by('-created_date'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


@page_template('article/articles_index_page.html')
def new(request, template='article/articles.html',
        extra_context=None):
    context = {
        'article': Article.objects.all().order_by('-created_date'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


@login_required
def new_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        formset = ImageForm(request.POST, request.FILES)
        located = Zone(request.POST)
        if form.is_valid() and formset.is_valid() and located.is_valid():
            postForm = form.save(commit=False)
            postForm.author = request.user
            postForm.created_date = datetime.now()
            postForm.save()
            form.save_m2m()
            location = located.save(commit=False)
            location.article = postForm
            location.save()
            files = request.FILES.getlist('image')
            for imgform in files:
                photo = Images(article=postForm, image=imgform)
                photo.save()
            return redirect('/new/')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Something went wrong.')
    else:
        located = Zone()
        form = ArticleForm()
        formset = ImageForm()
    return render(request, 'article/new.html', {
        'form': form,
        'imageform': formset,
        'located': located})


@login_required
def like(request):
    if request.is_ajax():
        user = request.user
        article_id = request.POST['article']
        article = Article.objects.get(pk=article_id)
        like = Likes.objects.filter(author=user, article=article)
        if like:
            like.delete()
        else:
            like = Likes(author=user, article=article)
            like.save()
        return HttpResponse(article.get_likes())


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    located = PointOfInterest.objects.get(article=pk)
    return render(request, 'article/article.html', {
        'article': article,
        'location': located})


@login_required
def comment(request):
    if request.method == "POST":
        article_id = request.POST['article']
        article = Article.objects.get(pk=article_id)
        comment = request.POST['comment']
        comment = comment.strip()
        if len(comment) > 0:
            article_comment = Comment(user=request.user,
                                      article=article,
                                      comment=comment)
            article_comment.save()
        html = ''
        for comment in article.get_comments():
            html = '{0}{1}'.format(html, render_to_string(
                'article/article_comment.html',
                {'comment': comment}))
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest()


@login_required
def edit(request, pk):
    post = get_object_or_404(Article, pk=pk)
    located = PointOfInterest.objects.get(article=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=post)
        location = Zone(request.POST, instance=located)
        if form.is_valid() and location.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            locate = location.save(commit=False)
            locate.article = post
            locate.save()
            return redirect('article_detail', pk=post.pk)
    else:
        form = ArticleForm(instance=post)
        location = Zone(instance=located)
    return render(request, 'article/edit.html', {
                 'form': form, 'location': location})


@login_required
def remove(request):
    comment_id = request.POST['comment']
    comment = Comment.objects.get(pk=comment_id)
    if request.user == comment.user:
        comment.delete()
        return HttpResponse()


@login_required
def delete_article(request):
    post_id = request.POST.get('post')
    post = Article.objects.get(pk=post_id)
    if request.user == post.author:
        post.delete()
        return HttpResponse()
