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
import datetime

class sale_order(osv.osv):
    _inherit = "sale.order"

    def expand_packs(self, cr, uid, ids, context={}, depth=1):
        super(sale_order, self).expand_packs(cr, uid, ids, context, depth)
        line_obj = self.pool.get('sale.order.line')
        for order in self.browse(cr, uid, ids, context):
            for line in order.order_line:
                if line.product_id:
                    if line.product_id.subscription and line.subscription_end_date and line.subscription_start_date and line.pack_child_line_ids:
                        for subline in line.pack_child_line_ids:
                            line_obj.write(cr, uid, subline.id, {'price_unit': 0})
        return

    def compute_delivery_dates(self, cr, uid, ids):
        line_obj = self.pool.get('sale.order.line')
        for order in self.browse(cr, uid, ids):
            for line in order.order_line:
                if line.product_id and line.product_id.subscription and line.subscription_end_date and line.subscription_start_date and line.pack_child_line_ids:
                    start_date = datetime.datetime.strptime(line.subscription_start_date, '%Y-%m-%d')
                    duration = (datetime.datetime.strptime(line.subscription_end_date, '%Y-%m-%d') - start_date).days
                    delta = datetime.timedelta(duration / len(line.pack_child_line_ids))
                    current_date = start_date
                    for subline in line.pack_child_line_ids:
                        current_date = current_date + delta
                        for move in subline.move_ids:
                            self.pool.get('stock.move').write(cr, uid, [move.id], {
                                'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                                'date_expected': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                                })
        return True

    def action_ship_create(self, cr, uid, ids, *args):
        res = super(sale_order, self).action_ship_create(cr, uid, ids, *args)
        self.compute_delivery_dates(cr, uid, ids)
        return res

sale_order()

