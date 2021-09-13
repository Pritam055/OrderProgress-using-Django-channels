from django.db.models.fields import CharField
from django.http.response import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
import json 

from .models import Momo, Order
# Create your views here.
class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['momos'] = Momo.objects.all()
        context['orders'] = Order.objects.all()
        return context


def order_progress(request, order_token):
    order = Order.objects.filter(order_token = order_token).first()
    if order is None:
        return redirect('/')
    return render(request, 'home/order.html', {'order': order})

@csrf_exempt
def order_momo(request):
    data = json.loads(request.body)
    try:
        momo = Momo.objects.get(id=data['id'])
        order =Order(momo=momo, amount=momo.price, user = request.user)
        order.save()
        return JsonResponse({"status": "success"})
    except Momo.DoesNotExist:
        return JsonResponse({"status": "Something went worong."})