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

from osv import osv, fields
from tools.translate import _

class email_template(osv.osv):
    _inherit = 'email.template'

    def _get_order_line_model_id(self, cr, uid, fields, context=None):
        return self.pool.get('ir.model').search(cr, uid, [('model', '=', 'sale.order.line')])[0]

    _defaults = {
        'object_name': _get_order_line_model_id,
        'def_to': '${object.order_id.partner_id.email}',
        'def_cc': '${object.order_id.shop_id.company_id.partner_id.email}',
        }

email_template()