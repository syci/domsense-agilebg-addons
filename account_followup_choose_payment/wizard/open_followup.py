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
import time
from datetime import datetime
from datetime import timedelta
import calendar

class account_followup_open(osv.osv_memory):
    _name = "account.followup.open"
    _columns = {
        'date': fields.date('Follow-up Sending Date', required=True, help="This field allow you to select a forecast date to plan your follow-ups"),
        'followup_id': fields.many2one('account_followup.followup', 'Follow-up', required=True)
    }

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def account_followup_open_window(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        mod_obj = self.pool.get('ir.model.data')
        move_line_pool = self.pool.get('account.move.line')
        fup_line_pool = self.pool.get('account_followup.followup.line')
        if context is None:
            context = {}
        form_data = self.read(cr, uid, ids, [], context=context)[0]
        context['fup_printing_date'] = form_data['date']
        context['current_fup_id'] = form_data['followup_id']
        move_line_ids = move_line_pool.search(cr, uid, [
            '&','&','&','&','|',('followup_line_id','=',False),('followup_line_id.followup_id','=',form_data['followup_id']),
            ('account_id.type','=','receivable'),('credit','=',0),('reconcile_id','=',False),('partner_id','!=',False)
            ])
        displayed_line_ids = []
        fup_line_ids = fup_line_pool.search(cr, uid, [('followup_id', '=', form_data['followup_id'])])
        for move_line in move_line_pool.browse(cr, uid, move_line_ids, context):
            for fup_line in fup_line_pool.browse(cr, uid, fup_line_ids, context):
                date_maturity = datetime.strptime(move_line.date_maturity or move_line.date, '%Y-%m-%d')
                delay = timedelta(fup_line.delay)
                expiration = date_maturity + delay
                if fup_line.start == 'end_of_month':
                    expiration = expiration.replace(day=calendar(expiration.year, expiration.month)[1])
                if expiration < datetime.strptime(form_data['date'], '%Y-%m-%d'):
                    if move_line.followup_line_id and fup_line.sequence > move_line.followup_line_id.sequence \
                        or not move_line.followup_line_id:
                        if move_line.id not in displayed_line_ids:
                            displayed_line_ids.append(move_line.id)

        res = mod_obj.get_object_reference(cr, uid, 'account_followup_choose_payment', 'view_fups_tree')
        res_id = res and res[1] or False
        filter_res = mod_obj.get_object_reference(cr, uid, 'account_due_list', 'view_payments_filter')
        filter_res_id = filter_res and filter_res[1] or False
        id_domain = [('id','=',0)]

        for displayed_line_id in displayed_line_ids:
            if id_domain == [('id','=',0)]:
                id_domain = [('id','=',displayed_line_id)]
            else:
                id_domain.append(('id','=',displayed_line_id))
                id_domain.insert(0, '|')

        return {
            'name': 'Follow-Ups to send',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': [res_id],
            'search_view_id': [filter_res_id],
            'res_model': 'account.move.line',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': id_domain,
            'context': context,
        }

account_followup_open()
