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
    'name': "Analytic Deferred Choice for Invoices",
    'version': '0.1',
    'category': 'Generic Modules/Accounting',
    'description': """User can assign the invoice amount to one or more analytic accounts, subsequently (or previously) to invoice confirmation.
    The invoice has a new field, containing the analytic plan to be used. The related button generates tha analytic lines, related to the invoice. The invoice lines have new fields too, containing the analytic plan. If the line's field is not filled, the invoice's one is used.
    On the invoice form, another button allows to delete the previously generated analytic lines.
    Every analytic line contains a reference to the invoice line that generated it.""",
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends" : ['account_analytic_plans'],
    "init_xml" : [],
    "update_xml" : [
        'account_invoice_view.xml',
        'project_view.xml',
        ],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
