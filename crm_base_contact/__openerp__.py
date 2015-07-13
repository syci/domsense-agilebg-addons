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
    "name": "CRM Base Contact",
    "version": "1.0",
    'category': 'Generic Modules/CRM & SRM',
    "depends": ["crm", "base_contact"],
    "author": "Agile Business Group",
    "description": """This module extends CRM partner creation with partner contacts""",
    'website': 'http://www.agilebg.com',
    'init_xml': [],
    'update_xml': [
    	'crm_lead_view.xml'
        ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
