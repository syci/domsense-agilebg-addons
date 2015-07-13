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

class crossovered_budget(osv.osv):
    _inherit = "crossovered.budget"
    
    _columns = {
        'state' : fields.selection([
            ('draft','Draft'),
            ('confirm','Confirmed'),
            ('validate1','Waiting second approval'),
            ('validate2','Waiting third approval'),
            ('validate','Validated'),
            ('done','Done'),
            ('cancel', 'Cancelled')], 'Status', select=True, required=True, readonly=True),
        'validating1_user_id': fields.many2one('res.users', 'Pre-Validate 1 User', readonly=True),
        'validating2_user_id': fields.many2one('res.users', 'Pre-Validate 2 User', readonly=True),
    }

    def budget_validate1(self, cr, uid, ids, *args):
        return self.write(cr, uid, ids, {
            'state': 'validate1',
            'validating1_user_id': uid,
        })

    def budget_validate2(self, cr, uid, ids, *args):
        return self.write(cr, uid, ids, {
            'state': 'validate2',
            'validating2_user_id': uid,
        })

crossovered_budget()
