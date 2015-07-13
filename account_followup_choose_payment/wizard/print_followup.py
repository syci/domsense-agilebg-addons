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

class wizard_followup(osv.osv_memory):

    _name = "wizard.account.followup"

    def _get_next_fup_level(self, cr, uid, fup_level):
        fup_line_dict = {}
        # collecting lines of current fup
        for fup_line in fup_level.followup_id.followup_line:
            fup_line_dict[fup_line.sequence] = fup_line
        # establishing which must be the next level
        for fup_line_seq in sorted(fup_line_dict.iterkeys()):
            if fup_line_seq > fup_level.sequence:
                return fup_line_dict[fup_line_seq]
        raise osv.except_osv(_('Error!'), _('No higher level follow-ups to send'))

    def _get_first_fup_level(self, cr, uid, fup):
        fup_line_dict = {}
        # collecting lines of current fup
        for fup_line in fup.followup_line:
            fup_line_dict[fup_line.sequence] = fup_line
        # establishing which must be the next level
        for fup_line_seq in sorted(fup_line_dict.iterkeys()):
            return fup_line_dict[fup_line_seq]
        raise osv.except_osv(_('Error!'), _('No higher level follow-ups to send'))
        

    def print_followup(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
            
        line_pool = self.pool.get('account.move.line')
        fup_pool = self.pool.get('account_followup.followup')
        fup_line_pool = self.pool.get('account_followup.followup.line')

        partner_ids = []
        lines_by_partner_and_level = {}
        fup_id = context.get('current_fup_id', False)
        fup_printing_date = context.get('fup_printing_date', False)
        # checking if fup has been selected
        if not fup_id:
            raise osv.except_osv(_('Error!'), _('The follow-up has not been selected. Open follow-ups by the specific wizard'))

        fup = fup_pool.browse(cr, uid, fup_id)

        for move_line_id in context.get('active_ids', []):
            move_line = line_pool.browse(cr, uid, move_line_id)
            # checking if there are different fups already sent
            if move_line.followup_line_id and fup_id != move_line.followup_line_id.followup_id.id:
                raise osv.except_osv(_('Error!'), _('In the selection are presents payments belonging to different follow-ups'))
            # building printable dict
            if move_line.partner_id:
                if move_line.followup_line_id:
                    next_fup_level = self._get_next_fup_level(cr, uid, move_line.followup_line_id)
                else:
                    next_fup_level = self._get_first_fup_level(cr, uid, fup)
                key = (move_line.partner_id.id, next_fup_level.id)
                if key not in lines_by_partner_and_level:
                    lines_by_partner_and_level[key] = {}
                    lines_by_partner_and_level[key]['lines'] = []
                lines_by_partner_and_level[key]['lines'].append(move_line.id)
                lines_by_partner_and_level[key]['message'] = ''
                lines_by_partner_and_level[key]['message2'] = ''
                lines_by_partner_and_level[key]['fup_printing_date'] = fup_printing_date
                if next_fup_level.description:
                    lines_by_partner_and_level[key]['message'] = next_fup_level.description
                if next_fup_level.description2:
                    lines_by_partner_and_level[key]['message2'] = next_fup_level.description2

            # useless partner_ids (for 'ids')
            if move_line.partner_id and move_line.partner_id.id not in partner_ids:
                partner_ids.append(move_line.partner_id.id)

        for key in lines_by_partner_and_level:
            # writing nextlevel to move lines
            for move_line_id in lines_by_partner_and_level[key]['lines']:
                line_pool.write(cr, uid, [move_line_id], 
                    {'followup_line_id': key[1], 'followup_date': fup_printing_date})

        datas = {'ids': partner_ids}
        datas['model'] = 'res.partner'
        datas['form'] = {}
        datas['form']['lines_by_partner_and_level'] = lines_by_partner_and_level
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account_followup_choose_payment.followup',
            'datas': datas,
        }

wizard_followup()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
