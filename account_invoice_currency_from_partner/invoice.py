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

class account_invoice(osv.osv):
    
    _inherit = 'account.invoice'
    
    def onchange_partner_id(self, cr, uid, ids, type, partner_id,
        date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        res = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id,
            date_invoice=date_invoice, payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
            if type in ('out_invoice', 'out_refund'):
                if partner.property_account_receivable.currency_id:
                    res['value']['currency_id'] = partner.property_account_receivable.currency_id.id
            elif type in ('in_invoice', 'in_refund'):
                if partner.property_account_payable.currency_id:
                    res['value']['currency_id'] = partner.property_account_payable.currency_id.id
        return res
    
account_invoice()
