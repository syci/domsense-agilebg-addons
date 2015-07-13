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

class sale_order_line_master(osv.osv):

    _inherit = "sale.order.line.master"
    _columns = {
        "product_tmpl_id": fields.many2one('product.template', "Product Template"),
        'variant_line_ids': fields.one2many('product.select.variant.line', 'master_so_line_id', 'Variants'),
        }
    
    def pre_selection_changed(self, cr, uid, ids, product_tmpl_id, variant_line_ids):
        prod_ids = self.pool.get('account.invoice.line').search_products(
            cr, uid, product_tmpl_id, variant_line_ids=variant_line_ids)
        res = {'domain': {'product_id': [('id', 'in', prod_ids)]}}
        if len(prod_ids) == 1:
            res['value'] = {'product_id': prod_ids[0]}
        return res
        
    def generate_detailed_lines(self, cr, uid, ids, context=None):
        res = super(sale_order_line_master, self).generate_detailed_lines(
            cr, uid, ids, context=context)
        var_line_pool = self.pool.get('product.select.variant.line')
        for master_line in self.browse(cr, uid, ids, context=context):
            for order_line in master_line.order_line_ids:
                if master_line.product_tmpl_id:
                    order_line.write({'product_tmpl_id': master_line.product_tmpl_id.id})
                for variant_line in master_line.variant_line_ids:
                    var_line_pool.create(cr, uid, {
                        'dimension_id': variant_line.dimension_id.id,
                        'option_id': variant_line.option_id.id,
                        'so_line_id': order_line.id,
                        }, context=context)
        return res
        
sale_order_line_master()

class product_select_variant_line(osv.osv):

    _inherit = "product.select.variant.line"
    _columns = {
        'master_so_line_id': fields.many2one('sale.order.line.master', 'Master SO line'),
        }
product_select_variant_line()
