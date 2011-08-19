# -*- coding: utf-8 -*-

import gettext
from gettext import gettext as _

__languages = ["pt_BR"]
__language = gettext.translation("heidsql", "./locale", languages=__languages)
__language.install(True)



    
