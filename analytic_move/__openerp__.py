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
{
    'name': "Analytic Move",
    'version': '0.1',
    'category': 'Generic Modules/Accounting',
    'description': """When user manually creates analytic lines, he is now able to track source and destination of the amounts. That is, if user moves amounts from an account to another, he can see where those amounts come from.
    This is achieved by the 'analytic move' object, that allows to group analytic lines.""",
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends" : ['analytic', 'account'],
    "init_xml" : [],
    "update_xml" : [
        'analytic_view.xml',
        'security/ir.model.access.csv',
        ],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
