# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#    $Id$
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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Customer interface for project issues",
    'version': '0.1',
    'category': 'Generic Modules/CRM & SRM',
    'description': """A simplified interface for project issues in order to make them usable by customers for tickets""",
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends" : ['project_issue_sheet'],
    "init_xml" : [],
    "update_xml" : [
        'project_issue_view.xml',
        'project_issue_menu.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        ],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
