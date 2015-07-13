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
    "name": "Sale Subscriptions Alerts",
    "version": "1.0",
    'category': 'Generic Modules/Sales & Purchases',
    "depends": ["sale_subscriptions", "email_template"],
    "author": "Agile Business Group",
    "description": """This module allows to configure the notifications to send before subscription expiration""",
    'website': 'http://www.agilebg.com',
    'init_xml': [],
    'update_xml': [
        'alert_view.xml',
        'security/ir.model.access.csv',
        ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
