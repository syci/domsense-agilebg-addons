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
from tools.translate import _

class sale_order(osv.osv):
    _inherit = 'sale.order'
    def _make_invoice(self, cr, uid, order, lines, context=None):
        inv_id = super(sale_order, self)._make_invoice(cr, uid, order, lines, context)
        inv_obj = self.pool.get('account.invoice')
        if order.partner_shipping_id:
            inv_obj.write(cr, uid, [inv_id], {'address_shipping_id': order.partner_shipping_id.id}, context=context)
        return inv_id

sale_order()
