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

from osv import osv, fields

class sale(osv.osv):
    _inherit = "sale.order"

    def action_invoice_create(self, cr, uid, ids, grouped=False, 
            states=['confirmed', 'done', 'exception'], date_inv = False, context=None):
        result = super(sale, self).action_invoice_create(cr, uid, ids, grouped, 
            states, date_inv, context)
        obj_invoice = self.pool.get('account.invoice')
        for order in self.browse(cr, uid, ids, context={}):
            inv_ids = [x.id for x in order.invoice_ids]

            if order.journal_id.corrispettivi:
                obj_invoice.write(cr, uid, inv_ids, {
                    'corrispettivo': True,
                })

        return result

sale()
