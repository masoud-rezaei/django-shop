from django.shortcuts import render ,redirect
from django.urls import reverse
from .models import OrderItem ,Order
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
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

#generate pdf file 
def admin_order_pdf(request,order_id):
  #Create Bytestrame buffer
  buf=io.BytesIO()
  #Create a canvas 
  c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
  #create text object 
  textob =  c.beginText(id=order_id)
  textob.setTextOrigin(inch, inch)
  textob.setFont("Helvetica", 14)
  #Designate The model 
  orders = Order.objects.all()
  #create blank list 
  lines = []
  for order in orders:
    lines.append(order.first_name)
    lines.append(order.last_name)
    lines.append(order.email)
    lines.append(order.address)
    lines.append(order.postal_code)
    lines.append(order.paid)
    lines.append(" ")
  #loop
  for line in lines:
    textob.textLine(line)
  #finish up 
  c.drawText(textob)
  c.showPage()
  c.save()
  buf.seek(0)
  
  #return somethings 
  return FileResponse(buf,as_attachment=True,filename='admin_order_pdf')
  
    
def order_create(request):
  cart = Cart(request)
  if request.method == 'POST' :
    form = OrderCreateForm(request.POST)
    if form.is_valid():
      order = form.save(commit=False)
      if cart.coupon:
        order.coupon = cart.coupon
        order.discount = cart.coupon.discount
      order.save() 
      for item in cart:
        OrderItem.objects.create(order=order,
                                 product=item['product'],price=item['price'],quantity=item['quantity'])
      
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
                'orders/order/create.html',{'cart': cart, 'form': form})  
  
@staff_member_required
def admin_order_detail(request, order_id):
  order = get_object_or_404(Order, id=order_id)
  return render(request,
  'admin/orders/order/detail.html',{'order': order})
  
 
      