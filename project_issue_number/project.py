# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU AfferoGeneral Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv

class Project(osv.osv):
    _inherit = "project.project"

    _columns = {
        'issue_counter': fields.integer('Issue counter',default=0),
    }

    def _get_current_issue_counter(self, cr, uid, proj_id):
        return self.read(cr,uid,proj_id,['issue_counter'])['issue_counter']

    def _get_next_issue_number(self, cr, uid, proj_id):
        nr = self._get_current_issue_counter(cr, uid, proj_id) + 1
        # TODO: we should make this configurable as sequence
        return  "#%s" % nr

    def _decr_issue_counter(self, cr, uid, proj_id):
        current = self._get_current_issue_counter(cr, uid, proj_id)
        self.write(cr, uid, proj_id, {'issue_counter':current-1})

    def _incr_issue_counter(self, cr, uid, proj_id):
        current = self._get_current_issue_counter(cr, uid, proj_id)
        self.write(cr, uid, proj_id, {'issue_counter':current+1})


class Issue(osv.osv):
    _inherit = "project.issue"

    _columns = {
        'number': fields.char('Issue number', size=6),
    }

    def create(self, cr, uid, vals, context=None):
        pid = vals['project_id']
        proj = self.pool.get('project.project')
        next_number = proj._get_next_issue_number(cr,uid,pid)
        vals['number'] = next_number
        res = super(Issue,self).create(cr,uid,vals,context=context)
        proj._incr_issue_counter(cr,uid,pid)


    def unlink(self, cr, uid, ids, *args, **kwargs):
        if isinstance(ids,list):
            ids = ids[0]
        pid = self.read(cr,uid,ids,['project_id'])['project_id'][0]
        proj = self.pool.get('project.project')
        proj._decr_issue_counter(cr,uid,pid)
        return super(Issue,self).unlink(cr,uid,ids,*args,**kwargs)



