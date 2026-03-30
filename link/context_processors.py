from .models import Link, LinkBar

def global_link(request):
    link_data = Link.objects.filter(active=True).all()
    if LinkBar.objects.exists():
        link_bar_position = LinkBar.objects.all().first().position
        link_bar_justify = LinkBar.objects.all().first().justify
        link_bar_bgcolor = LinkBar.objects.all().first().bgcolor
        if LinkBar.objects.all().first().bgimage:
            link_bar_bgimage_url = LinkBar.objects.all().first().bgimage.url
        else:
            link_bar_bgimage_url = None
    else:
        link_bar_position = 'pre_footer'
        link_bar_justify = 'center'
        link_bar_bgcolor = '#ffffff'
        link_bar_bgimage_url = None
 
    return {'links': link_data, 
            'links_position': link_bar_position, 
            'links_justify': link_bar_justify, 
            'links_bgcolor': link_bar_bgcolor, 
            'links_bgimage_url': link_bar_bgimage_url}

def get_global_links():
    return Link.objects.filter(active=True).all()
