# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012
#    Agile Business Group sagl (<http://www.agilebg.com>)
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

from osv import fields,osv

class users(osv.osv):
    _inherit = "res.users"
    
    def _is_customer(self, cr, uid, ids, fieldc, arg, context=None):
        res = {}
        try:
            customer_group_id = self.pool.get('ir.model.data').get_object_reference(
                cr, uid, 'project_issue_customer_view', 'group_project_issue_customer')
        except ValueError:
            customer_group_id = False
        for user in self.browse(cr, uid, ids, context=context):
            res[user.id] = False
            if customer_group_id:
                for group in user.groups_id:
                    if group.id == customer_group_id[1]:
                        res[user.id] = True
                        break
        return res
    
    _columns = {
        'is_customer': fields.function(_is_customer, type='boolean', string="Is customer", store=True),
        }
