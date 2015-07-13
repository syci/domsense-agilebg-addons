# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Domsense s.r.l. (<http://www.domsense.com>).
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv

class account_invoice(osv.osv):
    _inherit = "account.invoice"

    def button_change_fiscal_position(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        fpos_obj = self.pool.get('account.fiscal.position')
        inv_line_obj = self.pool.get('account.invoice.line')
        
        for inv in self.browse(cr,uid,ids):
            for line in inv.invoice_line:
                new_taxes = fpos_obj.map_tax(cr, uid, inv.fiscal_position, line.product_id.taxes_id)
                inv_line_obj.write(cr, uid, [line.id], {'invoice_line_tax_id': [(6,0,new_taxes)]})

        return True

account_invoice()