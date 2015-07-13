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

from osv import osv
from osv import fields

class mail_compose_message(osv.osv_memory):
    
    _inherit = 'mail.compose.message'
    
    def get_message_data(self, cr, uid, message_id, context=None):
        res = super(mail_compose_message, self).get_message_data(cr, uid, message_id, context=context)
        mail_message = self.pool.get('mail.message')
        if message_id:
            message_data = mail_message.browse(cr, uid, message_id, context)
            res.update({
                'email_from' : message_data.email_to or current_user.user_email or False,
                })
        return res
mail_compose_message()
