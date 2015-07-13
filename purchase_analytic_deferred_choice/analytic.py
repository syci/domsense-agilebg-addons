# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
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

class account_analytic_line(osv.osv):
    _inherit = 'account.analytic.line'

    _columns = {
        'deferred_purchase_order_line_id': fields.many2one('purchase.order.line', 'Purchase Order Line', readonly=True),
        'deferred_purchase_order_id': fields.related('deferred_purchase_order_line_id', 'order_id', type="many2one",
            relation="purchase.order", string="Purchase Order", store=False, readonly=True),
        }

account_analytic_line()
