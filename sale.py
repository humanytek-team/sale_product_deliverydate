# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from datetime import datetime, timedelta, date
import pytz
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import UserError, RedirectWarning, ValidationError



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    def convert_tz(self, date):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        display_date_result = datetime.strftime(pytz.utc.localize(datetime.strptime(date,
        DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S") 
        return display_date_result


    # @api.multi
    # @api.onchange('product_delivery_date')
    # def onchange_deliverydate(self):
    #     for rec in self:
    #         sale_delay = rec.product_id.sale_delay
    #         create_date = self.order_id.date_order
    #         if create_date:
    #             create_date = self.convert_tz(create_date)
    #         product_delivery_date = False
    #         if create_date:
    #             create_date = datetime.strptime(str(create_date),"%Y-%m-%d %H:%M:%S")
    #             product_delivery_date = timedelta(days=(rec.product_id.sale_delay+1)) + create_date
    #             #rec.product_delivery_date = product_delivery_date
    #             new_product_delivery_date = rec.product_delivery_date
    #             new_product_delivery_date = datetime.strptime(str(new_product_delivery_date),"%Y-%m-%d")
    #             print 'new_product_delivery_date ',type(new_product_delivery_date)
    #             print 'new_product_delivery_date ',new_product_delivery_date
    #             print 'product_delivery_date: ',type(product_delivery_date)
    #             if new_product_delivery_date <= product_delivery_date:
    #                 rec.product_delivery_date = product_delivery_date
    #                 raise ValidationError(_('La fecha de entrega del producto no puede ser menor a '+str(product_delivery_date)))


    @api.multi
    @api.depends('product_id')
    def _compute_delivery_date(self):
        #print '_compute_delivery_date'
        for rec in self:
            #print '-----------'
            sale_delay = rec.product_id.sale_delay
            #create_date = rec.order_id.date_order
            create_date = rec.order_id.date_order
            #print 'self.order_id.create_date: ',self.order_id.create_date
            #print 'self.order_id.name: ',self.order_id.name
            if create_date:
                create_date = self.convert_tz(create_date)
            #create_date = rec.order_id.confirmation_date
            product_delivery_date = False
            if create_date:
                #print 'create_date: ',create_date
                create_date = datetime.strptime(str(create_date),"%Y-%m-%d %H:%M:%S")
                product_delivery_date = timedelta(days=(rec.product_id.sale_delay+1)) + create_date
                #print 'product_delivery_date: ',product_delivery_date
                rec.product_delivery_date = product_delivery_date
        return


    @api.multi
    def _set_delivery_date(self):
        print '_set_delivery_date'
        for rec in self:
            sale_delay = rec.product_id.sale_delay
            create_date = self.order_id.date_order
            #if create_date:
            #    create_date = self.convert_tz(create_date)
            product_delivery_date = False
            if create_date:
                create_date = self.convert_tz(create_date)
                create_date = datetime.strptime(str(create_date),"%Y-%m-%d %H:%M:%S")
                product_delivery_date = create_date
                #product_delivery_date = rec.order_id.date_order
                product_delivery_date = datetime.strptime(str(product_delivery_date),"%Y-%m-%d %H:%M:%S")
                #print 'product_delivery_date: ',product_delivery_date
                #print 'type product_delivery_date: ',type(product_delivery_date)
                #product_delivery_date = product_delivery_date.replace(hour=0,minute=0,second=0)
                product_delivery_date = product_delivery_date +timedelta(days=1)
                #print 'product_delivery_date: ',product_delivery_date
                #product_delivery_date = product_delivery_date.strftime("%Y-%m-%d %H:%M:%S")
                

                new_product_delivery_date = rec.product_delivery_date
                new_product_delivery_date = datetime.strptime(str(new_product_delivery_date),"%Y-%m-%d")
                new_product_delivery_date = new_product_delivery_date.replace(hour=23,minute=59,second=59)
                #print 'new_product_delivery_date: ',new_product_delivery_date
                if new_product_delivery_date <= product_delivery_date:
                    
                    
                    #print 'product_delivery_date CONVER: ',product_delivery_date
                    #rec.product_delivery_date = product_delivery_date
                    raise ValidationError(_('La fecha de entrega del producto '+rec.product_id.name+' no puede ser menor a '\
                        +str(product_delivery_date)+'.\nPor favor cambiela por otra.'))

    # @api.multi
    # def _set_delivery_date(self):
    #     print '_set_delivery_date'
    #     for rec in self:
    #         sale_delay = rec.product_id.sale_delay
    #         create_date = self.order_id.date_order
    #         if create_date:
    #             create_date = self.convert_tz(create_date)
    #         product_delivery_date = False
    #         if create_date:
    #             create_date = datetime.strptime(str(create_date),"%Y-%m-%d %H:%M:%S")
    #             product_delivery_date = timedelta(days=(rec.product_id.sale_delay+1)) + create_date
    #             #rec.product_delivery_date = product_delivery_date

    #             product_delivery_date = product_delivery_date.replace(hour=0,minute=0,second=0)

    #             new_product_delivery_date = rec.product_delivery_date
    #             new_product_delivery_date = datetime.strptime(str(new_product_delivery_date),"%Y-%m-%d")
    #             #print 'new_product_delivery_date ',new_product_delivery_date
    #             #print 'product_delivery_date ',product_delivery_date
    #             if new_product_delivery_date < product_delivery_date:
    #                 #rec.product_delivery_date = product_delivery_date
    #                 raise ValidationError(_('La fecha de entrega del producto '+rec.product_id.name+' no puede ser menor a '\
    #                     +str(product_delivery_date)+'.\nPor favor cambiela por otra.'))


    #product_delivery_date = fields.Date('Fecha de entrega')
    #line_date_order = fields.Datetime('Fecha de orden', related='order_id.date_order')
    product_delivery_date = fields.Date('Fecha de entrega',compute='_compute_delivery_date',inverse='_set_delivery_date',store=True)
