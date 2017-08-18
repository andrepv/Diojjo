

def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = None
    if not user.profile.avatar:
        if backend.name == 'facebook':
            url = "http://graph.facebook.com/%s/picture?width=200&height=200"%response['id']
        if backend.name == 'twitter':
            url = response.get('profile_image_url', '').replace('_normal', '')
        if backend.name == 'google-oauth2':
            url = response['image'].get('url').replace('sz=50', '')
        if url:
            user.profile.avatar = url
            user.save()
