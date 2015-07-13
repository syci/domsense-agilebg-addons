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

class account_invoice_line(osv.osv):

    _inherit = "account.invoice.line"
    _columns = {
        "product_tmpl_id": fields.many2one('product.template', "Product Template"),
        'variant_line_ids': fields.one2many('product.select.variant.line', 'invoice_line_id', 'Variants'),
        }
    
    def pre_selection_changed(self, cr, uid, ids, product_tmpl_id, variant_line_ids):
        prod_ids = self.search_products(cr, uid, product_tmpl_id, variant_line_ids=variant_line_ids)
        res = {'domain': {'product_id': [('id', 'in', prod_ids)]}}
        if len(prod_ids) == 1:
            res['value'] = {'product_id': prod_ids[0]}
        return res
        
    def search_products(self, cr, uid, product_tmpl_id, variant_line_ids=[], context=None):
        if context is None:
            context = {}
        prod_pool = self.pool.get('product.product')
        option_ids = []
        product_ids = []
        # collect options
        for variant in variant_line_ids:
            if variant[2] and variant[2].get('option_id', False) and variant[2]['option_id'] not in option_ids:
                option_ids.append(variant[2]['option_id'])
        # search for all variants of that template
        prod_ids = prod_pool.search(cr, uid, [('product_tmpl_id', '=', product_tmpl_id)],
            context=context)
        if option_ids:
            for prod in prod_pool.browse(cr, uid, prod_ids, context=context):
                options_found = 0
                for option_id in option_ids:
                    # find matching variants
                    if option_id in [dim.option_id.id for dim in prod.dimension_value_ids]:
                        options_found +=1
                # if product contains every selected option
                if options_found == len(option_ids):
                    product_ids.append(prod.id)
        else:
            product_ids = prod_ids
        return product_ids
        
account_invoice_line()

class product_select_variant_line(osv.osv):

    _name = "product.select.variant.line"
    _columns = {
        'dimension_id' : fields.many2one('product.variant.dimension.type', 'Dimension Type', required=True),
        'option_id' : fields.many2one('product.variant.dimension.option', 'Option', required=True),
        'invoice_line_id': fields.many2one('account.invoice.line', 'Invoice line'),
        }
product_select_variant_line()
