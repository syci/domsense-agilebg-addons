# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv

class super_order(osv.osv):
    
    def _get_fields_values(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        sale_pool = self.pool.get('sale.order')
        purchase_pool = self.pool.get('purchase.order')
        for super_order in self.browse(cr, uid, ids, context=context):
            res[super_order.id] = {}
            res[super_order.id]['company_id'] = eval(
                'super_order.'+super_order.type+'_order_id.company_id.id')
            res[super_order.id]['name'] = eval(
                'super_order.'+super_order.type+'_order_id.name')
            res[super_order.id]['date'] = eval(
                'super_order.'+super_order.type+'_order_id.date_order')
            res[super_order.id]['partner_id'] = eval(
                'super_order.'+super_order.type+'_order_id.partner_id.id')
            res[super_order.id]['invoiced_rate'] = eval(
                'super_order.'+super_order.type+'_order_id.invoiced_rate')
            res[super_order.id]['amount_untaxed'] = eval(
                'super_order.'+super_order.type+'_order_id.amount_untaxed')
            res[super_order.id]['amount_total'] = eval(
                'super_order.'+super_order.type+'_order_id.amount_total')
            state = eval(
                'super_order.'+super_order.type+'_order_id.state')
            res[super_order.id]['state'] = dict(eval(super_order.type+'_pool').fields_get(cr, uid, allfields=['state'], context=context)['state']['selection'])[state]
            res[super_order.id]['state_key'] = state
            if super_order.type  == 'sale':
                res[super_order.id]['delivered_rate'] = super_order.sale_order_id.picked_rate
            elif super_order.type  == 'purchase':
                res[super_order.id]['delivered_rate'] = super_order.purchase_order_id.shipped_rate
        return res

    def _get_super_order_by_sale(self, cr, uid, ids, context=None):
        result = []
        order_pool = self.pool.get('sale.order')
        super_order_pool= self.pool.get('super.order')
        for order in order_pool.browse(cr, uid, ids, context=context):
            super_order_ids = super_order_pool.search(cr, uid, [
                ('sale_order_id', '=', order.id),
                ], context=context)
            for super_order_id in super_order_ids:
                if super_order_id not in result:
                    result.append(super_order_id)
        return result

    def _get_super_order_by_purchase(self, cr, uid, ids, context=None):
        result = []
        order_pool= self.pool.get('purchase.order')
        super_order_pool= self.pool.get('super.order')
        for order in order_pool.browse(cr, uid, ids, context=context):
            super_order_ids = super_order_pool.search(cr, uid, [
                ('purchase_order_id', '=', order.id),
                ], context=context)
            for super_order_id in super_order_ids:
                if super_order_id not in result:
                    result.append(super_order_id)
        return result
        
    _name = 'super.order'
    _rec_name = 'type'
    _columns = {
        'type': fields.selection([
            ('sale', 'Sale'),
            ('purchase', 'Purchase'),
            ], 'Type', required=True, readonly=True),
        'sale_order_id': fields.many2one('sale.order', 'Sale Order', readonly=True, ondelete='cascade'),
        'purchase_order_id': fields.many2one('purchase.order', 'Purchase Order', readonly=True, ondelete='cascade'),
        'company_id': fields.function(_get_fields_values, string="Company", type="many2one", relation="res.company", multi="super", 
            store = {
                'super.order': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                'sale.order': (_get_super_order_by_sale, ['company_id'], 10),
                'purchase.order': (_get_super_order_by_purchase, ['company_id'], 10),
            }),
        'name': fields.function(_get_fields_values, string="Reference", type="char", size=64, multi="super", 
            store = {
                'super.order': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                'sale.order': (_get_super_order_by_sale, ['name'], 10),
                'purchase.order': (_get_super_order_by_purchase, ['name'], 10),
            }),
        'date': fields.function(_get_fields_values, string="Date", type="date", multi="super", 
            store = {
                'super.order': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                'sale.order': (_get_super_order_by_sale, ['date_order'], 10),
                'purchase.order': (_get_super_order_by_purchase, ['date_order'], 10),
            }),
        'partner_id': fields.function(_get_fields_values, string="Partner", type="many2one", relation="res.partner", multi="super", 
            store = {
                'super.order': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                'sale.order': (_get_super_order_by_sale, ['partner_id'], 10),
                'purchase.order': (_get_super_order_by_purchase, ['partner_id'], 10),
            }),
        'delivered_rate': fields.function(_get_fields_values, string="Delivered", type="float", multi="super"),
        'invoiced_rate': fields.function(_get_fields_values, string="Invoiced", type="float", multi="super"),
        'amount_untaxed': fields.function(_get_fields_values, string="Untaxed Amount", type="float", multi="super", 
            store = {
                'super.order': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                'sale.order': (_get_super_order_by_sale, ['amount_untaxed'], 10),
                'purchase.order': (_get_super_order_by_purchase, ['amount_untaxed'], 10),
            }),
        'amount_total': fields.function(_get_fields_values, string="Total", type="float", multi="super", 
            store = {
                'super.order': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                'sale.order': (_get_super_order_by_sale, ['amount_total'], 10),
                'purchase.order': (_get_super_order_by_purchase, ['amount_total'], 10),
            }),
        'state': fields.function(_get_fields_values, string="State", type="char", size=64, multi="super"),
        'state_key': fields.function(_get_fields_values, string="State", type="char", size=64, multi="super", 
            store = {
                'super.order': (lambda self, cr, uid, ids, c={}: ids, None, 10),
                'sale.order': (_get_super_order_by_sale, ['state'], 10),
                'purchase.order': (_get_super_order_by_purchase, ['state'], 10),
            }),
        }

class sale_order(osv.osv):
    _inherit = 'sale.order'
    def create(self, cr, uid, vals, context=None):
        res = super(sale_order, self).create(cr, uid, vals, context=context)
        self.pool.get('super.order').create(cr, uid, {
            'type': 'sale',
            'sale_order_id': res,
            }, context=context)
        return res

class purchase_order(osv.osv):
    _inherit = 'purchase.order'
    def create(self, cr, uid, vals, context=None):
        res = super(purchase_order, self).create(cr, uid, vals, context=context)
        self.pool.get('super.order').create(cr, uid, {
            'type': 'purchase',
            'purchase_order_id': res,
            }, context=context)
        return res
