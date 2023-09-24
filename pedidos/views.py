from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from carrinho.carrinho import Carrinho
from pedidos.forms import PedidoModelForm
from .models import ItemPedido, Pedido
from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class PedidoCreateView(CreateView):
    form_class = PedidoModelForm
    success_url = reverse_lazy('resumopedido')
    template_name = 'formpedido.html'

    def form_valid(self, form):
        car = Carrinho(request=self.request)
        pedido = form.save()

        for item in car:
            ItemPedido.objects.create(pedido=pedido,
                                      produto=item['produto'],
                                      preco=item['preco'],
                                      quantidade=item['quantidade'])

        car.limpar()
        self.request.session['idpedido'] = pedido.id

        # Send the confirmation email
        subject = 'Confirmation of Your Order'
        message = 'Thank you for your order!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [pedido.email]

        # Render the HTML template for the email
        html_message = render_to_string('email_template.html', {'pedido': pedido})

        # Send the email
        send_mail(
            subject,
            strip_tags(html_message),
            from_email,
            recipient_list,
            html_message=html_message,
        )

        return redirect('resumopedido', idpedido=pedido.id)
    

class ResumoPedidoTemplateView(TemplateView):
    template_name = 'resumopedido.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pedido'] = Pedido.objects.get(id=self.kwargs['idpedido'])
        return ctx