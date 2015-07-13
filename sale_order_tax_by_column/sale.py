# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#    $Id$
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
import decimal_precision as dp

class sale_order(osv.osv):

    _inherit = "sale.order"

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = super(sale_order, self)._amount_all(cr, uid, ids, field_name, arg, context=context)
        ''' # incompatible with current version of account_invoice_tax_by_column
        if self.pool.get('res.users').browse(cr, uid, uid).company_id.vertical_comp:
            precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Sale Price')
            ait_pool = self.pool.get('account.invoice.tax')
            cur_obj = self.pool.get('res.currency')
            for order in self.browse(cr, uid, ids, context=context):
                cur = order.pricelist_id.currency_id
                lines=[]
                for line in order.order_line:
                    line_dic = {'price_unit': line.price_unit, 'discount': line.discount,
                        'quantity': line.product_uom_qty, 'taxes': [], 'product': line.product_id}
                    for tax in line.tax_id:
                        line_dic['taxes'].append(tax)
                    lines.append(line_dic)
                
                tax_by_rate = ait_pool.compute_taxes_by_rate(cr, uid, lines=lines, precision=precision,
                    address_id=order.partner_invoice_id.id, partner=order.partner_id)
                amount_tax = 0.0
                for tax_amount in tax_by_rate.values():
                    amount_tax += tax_amount

                res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, amount_tax)
                res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        '''
        return res

    def _get_order(self, cr, uid, ids, context=None):
        return super(sale_order, self)._get_order(cr, uid, ids, context=context)

    _columns = {
        'amount_untaxed': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Sale Price'), string='Untaxed Amount',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The amount without tax."),
        'amount_tax': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Sale Price'), string='Taxes',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The tax amount."),
        'amount_total': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Sale Price'), string='Total',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The total amount."),
        }

sale_order()

