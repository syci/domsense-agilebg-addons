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

from osv import fields,osv

class sale_order_line(osv.osv):

    _inherit = "sale.order.line"
    _columns = {
        "product_tmpl_id": fields.many2one('product.template', "Product Template"),
        'variant_line_ids': fields.one2many('product.select.variant.line', 'so_line_id', 'Variants'),
        }
    
    def pre_selection_changed(self, cr, uid, ids, product_tmpl_id, variant_line_ids):
        prod_ids = self.pool.get('account.invoice.line').search_products(
            cr, uid, product_tmpl_id, variant_line_ids=variant_line_ids)
        res = {'domain': {'product_id': [('id', 'in', prod_ids)]}}
        if len(prod_ids) == 1:
            res['value'] = {'product_id': prod_ids[0]}
        return res
        
sale_order_line()

class product_select_variant_line(osv.osv):

    _inherit = "product.select.variant.line"
    _columns = {
        'so_line_id': fields.many2one('sale.order.line', 'SO line'),
        }
product_select_variant_line()
