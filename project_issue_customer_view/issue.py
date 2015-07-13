# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011-2012
#    Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011-2012 Domsense srl (<http://www.domsense.com>)
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

class project_issue(osv.osv):
    _inherit = "project.issue"
    
    def case_open(self, cr, uid, ids, *args):
        users_issues_mapping = {}
        for issue in self.browse(cr, uid, ids):
            users_issues_mapping[issue.id] = issue.user_id.id
        res = super(project_issue, self).case_open(cr, uid, ids, *args)
        for issue_id in users_issues_mapping:
            self.write(cr, uid, issue_id, {'user_id': users_issues_mapping[issue_id]})
        return res
        
    def _spent_hours(self, cr, uid, ids, name, args, context=None):
        res = {}
        for issue_id in ids:
            res[issue_id] = 0.0
            issue = self.browse(cr, uid, issue_id)
            if issue.task_id:
                res[issue_id] += issue.task_id.effective_hours
            for timesheet in issue.timesheet_ids:
                res[issue_id] += timesheet.line_id.unit_amount
        return res
        
    _columns = {
        'internal_notes': fields.text('Internal Notes'),
        'spent_hours': fields.function(_spent_hours, string="Spent Hours"),
        }

project_issue()
