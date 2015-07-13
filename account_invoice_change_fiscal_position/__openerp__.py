# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Domsense s.r.l. (<http://www.domsense.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Change fiscal position on invoices',
    'version': '0.1',
    'category': 'Generic Modules/Accounting',
    'description': """This module adds a button next to the fiscal position field
    in the invoice view that updates the invoice lines according to the new
    fiscal position.    
    """,
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com',
    'depends': ['base','account'],
    'init_xml': [],
    'update_xml': 
                [
                'account_invoice_view.xml',
                ],
    'demo_xml': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
