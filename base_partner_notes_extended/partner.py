# -*- encoding: utf-8 -*-
##################################################################################
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
##################################################################################

from osv import fields, osv

from tools.translate import _

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time


class res_partner_comments(osv.osv):
    _name = 'res.partner.comments'
    _description = 'Partner Note'
    _order = 'name desc'
    _columns = {
        'name':fields.datetime('Date'),
        'partner_id':fields.many2one('res.partner', 'Partner'),
        'comment':fields.text('Note'),
    }
    _defaults = {
        'name': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }


class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
        'comments_ids':fields.one2many('res.partner.comments', 'partner_id', 'Notes'),
    }