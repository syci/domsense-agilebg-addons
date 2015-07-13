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

class jasper_account_statement_wizard(osv.osv_memory):
    _name='jasper.account.statement.wizard'

    _columns = {
        'from_date' : fields.date('From', required=True),
        'to_date' : fields.date('To', required=True),
        'from_account' : fields.char('From account', size=16, required=True),
        'to_account' : fields.char('To account', size=16, required=True),
        'show_currency': fields.boolean('Show amount in secondary currency'),
        }
    _defaults = {
        }
    def start_report(self, cr, uid, ids, data, context=None):
        for wiz_obj in self.read(cr,uid,ids):
            if 'form' not in data:
                data['form'] = {}
            data['form']['from_date'] = wiz_obj['from_date']
            data['form']['to_date'] = wiz_obj['to_date']
            data['form']['from_account'] = wiz_obj['from_account']
            data['form']['to_account'] = wiz_obj['to_account']
            data['model'] = 'account.account'
            data['ids']=self.pool.get(data['model']).search(cr,uid,[])

            report_name = 'jasper_account_statement_currency' if wiz_obj['show_currency'] else 'jasper_account_statement'

            return {
                    'type': 'ir.actions.report.xml',
                    'report_name': report_name,
                    'datas': data,
            }
jasper_account_statement_wizard()
