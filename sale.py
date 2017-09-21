# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from datetime import datetime, timedelta, date
import pytz
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    # @api.onchange('product_id')
    # def _compute_delivery_date(self):
    #     sale_delay = self.product_id.sale_delay
    #     create_date = self.order_id.date_order
    #     #create_date = self.order_id.confirmation_date
    #     product_delivery_date = False
    #     if create_date:
    #         create_date = datetime.strptime(str(create_date),"%Y-%m-%d %H:%M:%S")
    #         product_delivery_date = timedelta(days=(self.product_id.sale_delay+1)) + create_date
    #         self.product_delivery_date = product_delivery_date
    #     return

    #SIRVE
    # @api.depends('product_id','order_id.date_order')
    # def _compute_delivery_date(self):
    #     #print '2--------'
    #     sale_delay = self.product_id.sale_delay
    #     create_date = self.order_id.date_order
    #     #create_date = self.order_id.confirmation_date
    #     product_delivery_date = False
    #     if create_date:
    #         create_date = datetime.strptime(str(create_date),"%Y-%m-%d %H:%M:%S")
    #         product_delivery_date = timedelta(days=(self.product_id.sale_delay+1)) + create_date
    #         self.product_delivery_date = product_delivery_date
    #     return



    # user_tz = self.env.user.tz or pytz.utc
    # local = pytz.timezone(user_tz)
    # display_date_result = datetime.strftime(pytz.utc.localize(datetime.strptime(your_date_or_datetime_info,
    # DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%d/%m/%Y %H:%M%S") 

    def convert_tz(self, date):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        display_date_result = datetime.strftime(pytz.utc.localize(datetime.strptime(date,
        DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S") 
        return display_date_result

    @api.multi
    @api.depends('product_id','order_id.date_order')
    def _compute_delivery_date(self):
        
        for rec in self:
            #print '-----------'
            sale_delay = rec.product_id.sale_delay
            create_date = rec.order_id.date_order
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


    #product_delivery_date = fields.Date('Fecha de entrega')
    product_delivery_date = fields.Date('Fecha de entrega',compute='_compute_delivery_date',store=True)
