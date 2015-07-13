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

from osv import fields,osv
from tools.translate import _

class wizard_sent_followup(osv.osv_memory):

    _name = "wizard.account.sent.followup"

    def print_sent_followup(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        line_pool = self.pool.get('account.move.line')
        fup_line_pool = self.pool.get('account_followup.followup.line')

        partner_ids = []
        lines_by_partner_and_level = {}

        for move_line_id in context.get('active_ids', []):
            move_line = line_pool.browse(cr, uid, move_line_id)
            if not move_line.followup_line_id:
                raise osv.except_osv(_('Error'), _('You are trying to print payments without previous follow-ups'))
            # building printable dict
            if move_line.partner_id:
                key = (move_line.partner_id.id, move_line.followup_line_id.id)
                if key not in lines_by_partner_and_level:
                    lines_by_partner_and_level[key] = {}
                    lines_by_partner_and_level[key]['lines'] = []
                lines_by_partner_and_level[key]['lines'].append(move_line.id)
                lines_by_partner_and_level[key]['message'] = ''
                lines_by_partner_and_level[key]['message2'] = ''
                lines_by_partner_and_level[key]['fup_printing_date'] = move_line.followup_date
                if move_line.followup_line_id.description:
                    lines_by_partner_and_level[key]['message'] = move_line.followup_line_id.description
                if move_line.followup_line_id.description2:
                    lines_by_partner_and_level[key]['message2'] = move_line.followup_line_id.description2

        datas = {'ids': partner_ids}
        datas['model'] = 'res.partner'
        datas['form'] = {}
        datas['form']['lines_by_partner_and_level'] = lines_by_partner_and_level
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account_followup_choose_payment.followup',
            'datas': datas,
        }

wizard_sent_followup()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
