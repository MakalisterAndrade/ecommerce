from django.shortcuts import render, reverse

from ecommerce import settings
from pagamentos.forms import CheckoutForm
from pedidos.models import Pedido
from django.views.generic import TemplateView, FormView
import braintree

class ProcessarPagamento(FormView):
    template_name = 'pagamento/processar.html'
    form_class = CheckoutForm

    def dispatch(self, request, *args, **kwargs):
        braintree_env = braintree.Environment.Sandbox
        braintree.Configuration.configure(braintree_env, merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                          public_key=settings.BRAINTREE_PUBLIC_KEY,
                                          private_key=settings.BRAINTREE_PRIVATE_KEY,)
        self.braintree_client_token = braintree.ClientToken.generate({})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['braintree_client_token'] = self.braintree_client_token
        return ctx
