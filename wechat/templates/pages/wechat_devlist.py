# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from math import ceil
from frappe import _

from wechat.api import check_wechat_binding
from iot_ui.ui_api import devices_list_array


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True

	try:
		app = check_wechat_binding()

		if frappe.session.user == 'Guest':
			frappe.local.flags.redirect_location = "/login"
			raise frappe.Redirect

		context.filter = frappe.form_dict.filter or "all"

		context.language = frappe.db.get_value("User", frappe.session.user, ["language"])
		context.csrf_token = frappe.local.session.data.csrf_token

		if 'Company Admin' in frappe.get_roles():
			context.isCompanyAdmin = True

		userdevices = devices_list_array(context.filter) or []
		context.userdevices = userdevices
		context.dev_lens = int(ceil(len(userdevices)*0.1))

		context.wechat_app = app or frappe.form_dict.app
		context.title = _('Wechat Devices')

	except Exception as ex:
		frappe.logger(__name__).exception(ex)
		raise ex
