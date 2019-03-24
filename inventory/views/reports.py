import datetime
import os

from django.views.generic import TemplateView

from . import models
from common_data.utilities import ConfigMixin
from inventory.views.common import CREATE_TEMPLATE
from wkhtmltopdf.views import PDFTemplateView

class InventoryReport( ConfigMixin, TemplateView):
    template_name = os.path.join('inventory', 'reports', 'inventory_report.html')

    def get_context_data(self, *args, **kwargs):
        context = super(InventoryReport, self).get_context_data(*args, **kwargs)
        context['items'] = models.WareHouseItem.objects.filter(item__type=0)
        context['date'] = datetime.date.today()
        context['pdf_link'] = True


        #insert config
        return context


class OutstandingOrderReport( ConfigMixin, TemplateView):
    template_name = os.path.join('inventory', 'reports', 'outstanding_orders.html')

    def get_context_data(self, *args, **kwargs):
        context = super(OutstandingOrderReport, self).get_context_data(*args, **kwargs)
        context['orders'] = models.Order.objects.all()
        context['date'] = datetime.date.today()
        context['pdf_link'] = True
        #insert config
        return context



class InventoryReportPDFView( ConfigMixin, PDFTemplateView):
    template_name = os.path.join('inventory', 'reports', 'inventory_report.html')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['items'] = models.WareHouseItem.objects.all()
        context['date'] = datetime.date.today()
        #insert config
        return context


class OutstandingOrderReportPDFView( ConfigMixin, PDFTemplateView):
    template_name = os.path.join('inventory', 'reports', 'outstanding_orders.html')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['orders'] = models.Order.objects.all()
        context['date'] = datetime.date.today()
        #insert config
        return context
