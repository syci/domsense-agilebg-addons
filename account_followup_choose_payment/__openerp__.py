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
    'name': "Follow-UP - Choose payments",
    'version': '0.1',
    'category': 'Generic Modules/Payment',
    'description': """

Based on account_followup, this modules allows to send follow-ups selecting the
single (overdue) payments you want to notify to customers.

Follow-Ups are configured through 'account_followup' module. The order
follow-ups are sent with is set by the sequence field.

There are two main macro-functionalities:
- Print follow-ups (increasing follow-up level)
- Re-print old follow-ups

Print follow-ups
----------------

From the 'Open Follow-Ups' wizard, user can select the follow-up and the date.
From the opened list, user can select the payments he want to notify. Payments
can refer to several partners, due dates and previously notified follow-ups.
After clicking 'Print Follow-UP', payments are grouped by partner and last
follow-up level, if any. For each group, composed by a certain partner and
level, the system increases the follow-up level of every selected payment and
prints the group in a PDF page. If no further levels are available, a warning
will appear.

Re-print old follow-ups
-----------------------

Opening the 'Sent Follow-Ups' list, user can choose to re-print some old
follow-ups. As for new follow-ups, user can select several payments. The system
groups payments by partner and follow-up level and prints each group in a PDF
page. This time follow-up level will not be increased.

For more info: http://planet.domsense.com/en/2011/12/new-follow-up-module-for-openerp/
""",
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends" : ['account_followup', 'account_due_list', 'report_webkit'],
    "init_xml" : [],
    "update_xml" : [
        'wizard/print_followup.xml',
        'reports.xml',
        'wizard/open_followup.xml',
        'payment_view.xml',
        'wizard/print_sent_followup.xml',
        'account_followup_view.xml',
        ],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
