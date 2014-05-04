import json
from django.core import serializers
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.template import RequestContext, loader, Context
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from wms.models import Client, ReferredClients, Sku, Order, OrderDetail, Incoming, IncomingDetail
from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
    return render_to_response('wms/main.html')

@login_required
def main(request):
    return render_to_response('wms/main.html', context_instance=RequestContext(request))

@login_required
def client(request):
    available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
    return render_to_response('wms/client.html', {'available_clients':available_clients}, context_instance=RequestContext(request))

@login_required
def sku(request):
    available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
    available_sku=Sku.objects.select_related('client').filter(holder=available_clients)
    return render_to_response('wms/sku.html', {'available_sku':available_sku}, context_instance=RequestContext(request))

@login_required
def order(request):
    available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
    available_orders=Order.objects.select_related('client').filter(holder=available_clients)
    available_order_details=OrderDetail.objects.select_related('order').filter(order=available_orders)
    return render_to_response('wms/order.html', {'available_orders':available_orders, 'available_order_details':available_order_details}, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def order_detail(request):
    message = "0"
    print(request.method)
    print(request.POST)
    id=request.POST.get('id')
    a = {'id': 1}
    current_order_details=OrderDetail.objects.filter(order=id)
    b= current_order_details
    ans = {'id': str(current_order_details)}
    serialized_queryset = serializers.serialize('json', OrderDetail.objects.filter(order=id))
    print(serialized_queryset)
    print(a)
    print(b)
    print(ans)
    return HttpResponse(json.dumps(serialized_queryset,
            ensure_ascii=False), content_type='application/json')

@login_required
def incoming(request):
    available_clients=Client.objects.select_related('client').filter(referredclients__user=request.user.id)
    available_incomings=Incoming.objects.select_related('client').filter(holder=available_clients)
    return render_to_response('wms/incoming.html', {'available_incomings':available_incomings}, context_instance=RequestContext(request))

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')