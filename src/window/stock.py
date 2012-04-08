# -*- coding: utf-8 -*-

import gtk
import utils
import os


__DOMAIN = "icon_host"

__itens = []


STOCK_SERVER = "server"
__itens.append((STOCK_SERVER, _("Server"), 0, 0, __DOMAIN))

STOCK_DATABASE = "database"
__itens.append((STOCK_DATABASE, _("Database"), 0, 0, __DOMAIN))

STOCK_TABLE = "table"
__itens.append((STOCK_DATABASE, _("Table"), 0, 0, __DOMAIN))


STOCK_NAMESPACE = "namespace"
__itens.append((STOCK_NAMESPACE, _("Namespace"), 0, 0, __DOMAIN))

gtk.stock_add(__itens)

__factory = gtk.IconFactory()

for png in os.listdir(utils.get_res_icons("")):
    image = gtk.Image()
    image.set_from_file(utils.get_res_icons(png))
    pixbuf = image.get_pixbuf()
    __factory.add(os.path.basename(png)[:-4], gtk.IconSet(pixbuf))


__factory.add_default()


