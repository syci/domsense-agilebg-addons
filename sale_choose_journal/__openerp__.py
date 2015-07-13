# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#    $Id$
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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Select in the sale order the journal used for invoicing ",
    'version': '0.1',
    'category': 'Generic Modules/Accounting',
    'description': """
    This module adds a Journal field in the sale order.
    If you choose a journal here, invoices create from the order will have
    the selected journal.
""",
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends" : ['sale', 'account'],
    "init_xml" : [],
    "update_xml" : ['sale_view.xml'],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
