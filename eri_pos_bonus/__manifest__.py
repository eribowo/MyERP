# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Point of Sale Bonus, Gift, Loyalty addon',
    'version': '1.5',
    'category': 'Point of Sale',
    'sequence': 1,
    'summary': 'Point system for POS, POS Bonus, POS Loyalty, POS Gift, POS coupon, Point of sale Bonus, Point of sale Loyalty, Loyalty, Bonus, Coupon, Gift',
    'description': """

=======================

This module works same as enterprise version. This module allows you to define a loyalty program in
the point of sale, where the customers earn loyalty points
and get rewards.

""",
    'author': 'eribowo',
    'license': 'AGPL-3',
    'currency': 'EUR',
    'depends': ['point_of_sale'],
    'images': [
        'static/images/main_screenshot.png',
        'static/images/screenshot0.png',
        'static/images/screenshot01.png',
        'static/images/screenshot02.png',
        'static/images/screenshot03.png',
        'static/images/screenshot04.png',
        'static/images/screenshot05.png',
        'static/images/screenshot_main.png',
    ],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
        'views/templates.xml'
    ],
    'qweb': ['static/src/xml/loyalty.xml'],
    'installable': True,

}
