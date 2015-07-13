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
    'name': "Account Parallel Currency",
    'version': '0.1',
    'category': 'Generic Modules/Accounting',
    'description': """
    This module handles parallel accounting entries based on different currencies.
    It is useful for companies who have to manage accounting with more than one currency at the same time. For instance, companies who have to produce balances on different currencies.
    
    In order to use the module, you have to define one company for each parallel chart of accounts. Then you have to map parallel accounts and parallel journals through the related forms.
    
    A 'Parallel Account Mapping' wizard is provided. It is intended to be run when the same chart of account is used for the parallel companies. It allows to automatically map the 'master' account to 'parallel' accounts, based on account code.
    
    When posting new journal entries, the system checks the configured parallel accounts and automatically generates the parallel entries.
    For each user, it is possible to configure a 'parallel user' (that should be associated to a dummy parent company), used to carry out the parallel registrations. This allows to keep the companies separate, so that users of the master company don't see secondary company data (e.g. currencies and journals) but the system uses his parallel user in order to perform the parallel registrations.
    """,
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends" : ['account'],
    "init_xml" : [],
    "update_xml" : [
        'account_view.xml',
        'company_view.xml',
        'wizard/do_mapping.xml',
        'user_view.xml',
        'security/security.xml',
        ],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
