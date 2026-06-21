from business.models import Business


def business_context(request):
    business = Business.objects.filter(is_published=True).first()
    return {"business": business}
