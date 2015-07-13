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

import time
from report import report_sxw
from osv import osv

class Parser(report_sxw.rml_parse):

    def _get_partners_and_levels(self):
        res = []
        partner_pool = self.pool.get('res.partner')
        fup_line_pool = self.pool.get('account_followup.followup.line')
        for partner_id, level_id in self.localcontext['data']['form']['lines_by_partner_and_level']:
            res.append((partner_pool.browse(self.cr, self.uid, partner_id), fup_line_pool.browse(self.cr, self.uid, level_id)))
        return res

    def _get_message(self, partner_id, level_id):
        partner = self.pool.get('res.partner').browse(self.cr, self.uid, partner_id)
        text= self.localcontext['data']['form']['lines_by_partner_and_level'][(partner_id,level_id)]['message']
        if text:
            text = text % {
                'partner_name': partner.name,
                'date': time.strftime('%Y-%m-%d'),
                'company_name': self.localcontext['company'].name,
                'user_signature': self.pool.get('res.users').browse(self.cr, self.uid, self.uid).signature,
            }
        return text.replace('\n', '<br/>')

    def _get_message2(self, partner_id, level_id):
        partner = self.pool.get('res.partner').browse(self.cr, self.uid, partner_id)
        text= self.localcontext['data']['form']['lines_by_partner_and_level'][(partner_id,level_id)]['message2']
        if text:
            text = text % {
                'partner_name': partner.name,
                'date': time.strftime('%Y-%m-%d'),
                'company_name': self.localcontext['company'].name,
                'user_signature': self.pool.get('res.users').browse(self.cr, self.uid, self.uid).signature,
            }
        return text.replace('\n', '<br/>')

    def _get_inv_address_by_partner(self, partner_id):
        res = self.pool.get('res.partner').address_get(self.cr, self.uid, [partner_id], adr_pref=['invoice'])
        return self.pool.get('res.partner.address').browse(self.cr, self.uid, res['invoice'])

    def _get_lines_by_partner_and_level(self, partner_id, level_id):
        line_ids = self.localcontext['data']['form']['lines_by_partner_and_level'][(partner_id,level_id)]['lines']
        return self.pool.get('account.move.line').browse(self.cr, self.uid, line_ids)

    def _get_partner_balance(self, partner_id, level_id):
        line_ids = self.localcontext['data']['form']['lines_by_partner_and_level'][(partner_id,level_id)]['lines']
        balance = 0.0
        for move_line in self.pool.get('account.move.line').browse(self.cr, self.uid, line_ids):
            balance += (move_line.debit - (
                move_line.reconcile_partial_id and self._get_line_amount_paid(move_line.reconcile_partial_id.id) or 0.0))
        return balance

    def _get_line_amount_paid(self, reconcile_id):
        reconcile = self.pool.get('account.move.reconcile').browse(self.cr, self.uid, reconcile_id)
        total = 0.0
        for line_partial_id in reconcile.line_partial_ids:
            total += line_partial_id.credit
        return total

    def _get_fup_printing_date(self, partner_id, level_id):
        return self.localcontext['data']['form']['lines_by_partner_and_level'][(partner_id,level_id)]['fup_printing_date']

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'partners_and_levels': self._get_partners_and_levels,
            'lines_by_partner_and_level': self._get_lines_by_partner_and_level,
            'inv_address_by_partner': self._get_inv_address_by_partner,
            'message': self._get_message,
            'message2': self._get_message2,
            'fup_printing_date': self._get_fup_printing_date,
            'line_amount_paid': self._get_line_amount_paid,
            'partner_balance': self._get_partner_balance,
        })

report_sxw.report_sxw('report.account_followup_choose_payment.followup',
                       'account_followup_choose_payment.followup', 
                       'account_followup_choose_payment/templates/followup.mako',
                       parser=Parser)
