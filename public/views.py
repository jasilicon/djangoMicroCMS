from django.shortcuts import render, get_object_or_404
from business.models import Business


def home(request, slug=None):
    if slug:
        business = get_object_or_404(Business, slug=slug, is_published=True)
    else:
        business = Business.objects.filter(is_published=True).first()

    if not business:
        return render(request, "public/setup.html")

    sections = {
        s.section_slug: s.is_published
        for s in business.section_publishes.all()
    }
    hero_images = business.hero_images.filter(is_published=True)
    gallery = business.gallery_images.filter(is_published=True)
    service_categories = business.service_categories.filter(is_published=True).prefetch_related("services")
    hours = business.business_hours.all()
    social_links = business.social_links.filter(is_published=True)

    return render(request, "public/home.html", {
        "business": business,
        "sections": sections,
        "hero_images": hero_images,
        "gallery": gallery,
        "service_categories": service_categories,
        "hours": hours,
        "social_links": social_links,
    })
