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
from tools.translate import _

class stock_picking(osv.osv):
    def _compute_qty(self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for move in picking.move_lines:
                total += move.product_qty
            res[picking.id] = total
        return res
        
    def _compute_total_qty(self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            total = picking.qty
            for child in picking.child_ids:
                total += child.qty
            res[picking.id] = total
        return res
        
    def _compute_uom(self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            uom = ''
            for move in picking.move_lines:
                if uom and move.product_uom.name != uom:
                    uom = _('Various')
                else:
                    uom = _(move.product_uom.name)
            res[picking.id] = uom
        return res
    
    _inherit = "stock.picking"
    _columns = {
        'parent_id': fields.many2one('stock.picking', 'Parent Picking', readonly=True),
        'child_ids': fields.one2many('stock.picking', 'parent_id', 'Children Pickings', readonly=True),
        'qty': fields.function(_compute_qty, string="Quantity"),
        'total_qty': fields.function(_compute_total_qty, string="Total Quantity"),
        'uom': fields.function(_compute_uom, string="UoM", type='char',
            size=64),
        }
        
    def do_partial(self, cr, uid, ids, partial_datas, context=None):
        res = super(stock_picking, self).do_partial(cr, uid, ids, partial_datas, context=context)
        for pick_id in res:
            if res[pick_id].get('delivered_picking', False):
                if res[pick_id]['delivered_picking'] != pick_id:
                    self.write(cr, uid, res[pick_id]['delivered_picking'], {'parent_id': pick_id})
                
        return res
        
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        default['parent_id'] = False
        default['child_ids'] = False
        return super(stock_picking, self).copy(cr, uid, id, default, context)
        
stock_picking()
