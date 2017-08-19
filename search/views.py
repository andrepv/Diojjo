from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from endless_pagination.decorators import page_template
from django.template import RequestContext

from article.models import Article


@page_template('article/articles_index_page.html')
def search(request, template='search/results.html', extra_context=None):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/')
        context = {
            'article': Article.objects.filter(
                Q(title__icontains=querystring) |
                Q(text__icontains=querystring))
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(
            template, context, context_instance=RequestContext(request))
    else:
        return redirect('/')


@page_template('article/articles_index_page.html')
def tag(request, tag_name, template='article/articles.html',
        extra_context=None):
    context = {
        'article': Article.objects.filter(tags__name=tag_name)
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))
