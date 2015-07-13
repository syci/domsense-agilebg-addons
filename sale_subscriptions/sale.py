# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Domsense s.r.l. (<http://www.domsense.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields,osv
import time
import netsvc
import datetime
from tools.translate import _

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    _columns =  {
        'subscription': fields.related('product_id', 'subscription', type='boolean', string='Subscription'),
        'subscription_start_date':fields.date('Subscription Beginning Date', readonly=True, states={'draft': [('readonly', False)]}),
        'subscription_end_date':fields.date('Subscription Ending Date', readonly=True, states={'draft': [('readonly', False)]}),
        'cron_ids': fields.one2many('ir.cron', 'subscription_id', 'Cron'),
    }

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        result_dict = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag, context)
        if product:
            product = self.pool.get('product.product').browse(cr, uid, product)
            if product.subscription and product.subscription_duration:
                subscription_start_date = time.strftime('%Y-%m-%d')
                duration_delta = datetime.timedelta(0,product.subscription_duration * 24 * 60 * 60)
                start_date = datetime.datetime.strptime(subscription_start_date, '%Y-%m-%d')
                end_date = start_date + duration_delta
                subscription_end_date = end_date.strftime('%Y-%m-%d')
                result_dict['value'].update({
                    'subscription_start_date': subscription_start_date,
                    'subscription_end_date': subscription_end_date,
                    })
        return result_dict

sale_order_line()

class sale_order(osv.osv):
    _inherit = "sale.order"
    _logger = netsvc.Logger()

    def new_order(self, cr, uid, line_id, context=None):

        line_obj = self.pool.get('sale.order.line')
        line = line_obj.browse(cr, uid, line_id)
        order_obj = self.pool.get('sale.order')
        order = order_obj.browse(cr, uid, line.order_id.id)
        order_data= {
            'partner_id': order.partner_id.id,
            'partner_invoice_id': order.partner_invoice_id.id,
            'partner_order_id': order.partner_order_id.id,
            'partner_shipping_id': order.partner_shipping_id.id,
            'shop_id': order.shop_id.id,
            'client_order_ref': order.client_order_ref,
            'incoterm': order.incoterm.id,
            'picking_policy': order.picking_policy,
            'order_policy': order.order_policy,
            'pricelist_id': order.pricelist_id.id,
            'project_id': order.project_id.id,
            'note': order.note,
            'invoice_quantity': order.invoice_quantity,
            'payment_term': order.payment_term.id,
            'fiscal_position': order.fiscal_position.id,
            'order_line': [],
            'origin' : order.name,
            }

        subscription_start_date = time.strftime('%Y-%m-%d')
        duration_delta = datetime.timedelta(0,line.product_id.subscription_duration * 24 * 60 * 60)
        start_date = datetime.datetime.strptime(subscription_start_date, '%Y-%m-%d')
        end_date = start_date + duration_delta
        subscription_end_date = end_date.strftime('%Y-%m-%d')

        line_data = {
            'name': line.name,
            'delay': line.delay,
            'product_id': line.product_id.id,
            'price_unit': line.price_unit,
            'tax_id': [(6, 0, [])],
            'type': line.type,
            'address_allotment_id': line.address_allotment_id.id,
            'product_uom_qty': line.product_uom_qty,
            'product_uom': line.product_uom.id,
            'product_uos_qty': line.product_uos_qty,
            'product_uos': line.product_uos.id,
            'product_packaging': line.product_packaging.id,
            'notes': line.notes,
            'discount': line.discount,
            'subscription_end_date': subscription_end_date,
            'subscription_start_date': subscription_start_date,
            }
        for tax in line.tax_id:
            line_data['tax_id'][0][2].append(tax.id)

        order_data['order_line'].append((0, 0, line_data))

        new_order_id = order_obj.create(cr, uid, order_data, context)
        self._logger.notifyChannel('sale_subscriptions', netsvc.LOG_INFO, "Order " + str(new_order_id) + " created")
        return new_order_id

    def action_wait(self, cr, uid, ids, *args):
        super(sale_order, self).action_wait(cr, uid, ids, *args)

        for o in self.browse(cr, uid, ids):
            for line in o.order_line:
                if line.subscription_end_date and line.subscription_start_date:
                    cron_data = {
                        'name': _('Subscription expiration: ') + line.name,
                        'nextcall' : line.subscription_end_date,
                        'model': 'sale.order',
                        'interval_number': 0,
                        'function': 'new_order',
                        'args': repr([line.id]),
                        'subscription_id': line.id,
                        }
                    self.pool.get('ir.cron').create(cr, uid, cron_data)
        return True

sale_order()

