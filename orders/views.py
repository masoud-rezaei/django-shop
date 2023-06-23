from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem, Order
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404 , HttpResponse
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


#from django .conf import settings
#from django.template.loader import render_to_string
#import weasyprint

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'], price=item['price'], quantity=item['quantity'])

            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payments:go-to-gateways'))
            # return render(request, 'orders/order/created.html',{'order':order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html', {'cart': cart, 'form': form})

 #order = get_object_or_404(Order,id=order_id)
    #response = HttpResponse(content_type='application/pdf')
   # response["Content-Disposition"] = f'filename=order_{order.id}.pdf'
# generate pdf file
def admin_order_pdf(request,order_id):
    #order = get_object_or_404(orders,id=order_id)
    # Create Bytestrame buffer
    buffer = io.BytesIO() 
    # Create a canvas
    p = canvas.Canvas(buffer ,pagesize=letter, bottomup=0)
    # create text object
    textob = p.beginText()
    textob.setTextOrigin(10 ,20)#inch, inch
    textob.setFont("Helvetica", 20)
    # Designate The model
    orders = Order.objects.get(pk=order_id) 
    # create blank list
    lines = []
    lines.append(orders.first_name)
    lines.append(orders.last_name)
    lines.append(orders.email)
    lines.append(orders.address)
    lines.append(orders.postal_code)
    lines.append(orders.city)
    lines.append(orders.paid)
    lines.append("###   ###   ###")
    # loop
    for line in lines:
        textob.textLine(line)
    # finish up
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)

    # return somethings
    return FileResponse(buffer, as_attachment=True, filename='admin_order_pdf.pdf')
    
                       
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html', {'order': order})
