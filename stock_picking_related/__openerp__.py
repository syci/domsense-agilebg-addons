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
{
    'name': "Hierarchic View for pickings",
    'version': '0.1',
    'category': 'Warehouse Management',
    'description': """This module helps to understand the relations between pickings.
    When a picking is partially delivered, it tracks every generated "child" picking. Equally, the generated picking refers to its "parent" picking.""",
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends" : ['stock'],
    "init_xml" : [],
    "update_xml" : [
        'stock_view.xml',
        ],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
