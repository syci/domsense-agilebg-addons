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
import netsvc
import datetime
from tools.translate import _

class sale_order(osv.osv):
    _inherit = "sale.order"
    _logger = netsvc.Logger()
    def action_wait(self, cr, uid, ids, *args):
        super(sale_order, self).action_wait(cr, uid, ids, *args)
        for o in self.browse(cr, uid, ids):
            for line in o.order_line:
                if line.subscription_end_date and line.subscription_start_date:
                    alert_obj = self.pool.get('subscription.alert')
                    date_start = datetime.datetime.strptime(line.subscription_start_date, '%Y-%m-%d')
                    date_end = datetime.datetime.strptime(line.subscription_end_date, '%Y-%m-%d')
                    days_delta = date_end - date_start
                    alert_ids = alert_obj.search(cr, uid, [('days_before', '>=', days_delta.days)])
                    for alert_id in alert_ids:
                        alert = alert_obj.browse(cr, uid, alert_id)
                        alert_delta = datetime.timedelta(0,alert.days_before * 24 * 60 * 60)
                        alert_date = datetime.datetime.strptime(line.subscription_end_date, '%Y-%m-%d')  - alert_delta
                        cron_data = {
                            'name': _('Alert: ') + line.name + ' - ' + alert.name,
                            'nextcall' : alert_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'model': 'email.template',
                            'interval_number': 0,
                            'function': 'generate_mail',
                            'args': repr([alert.template_id.id,[line.id]]),
                            'subscription_id': line.id,
                            }
                        self.pool.get('ir.cron').create(cr, uid, cron_data)
        return True

sale_order()

