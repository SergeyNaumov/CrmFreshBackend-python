from .tab.links import fields as fields_links
from .tab.main import fields as fields_main
from .tab.sale import fields as fields_sale
#from .tab.rekvizits import fields as fields_rekvizits
from .tab.paids import fields as fields_paids
from .tab.docpack import fields as fields_docpack


fields= fields_links + \
		fields_main + \
		fields_sale  + \
		fields_paids  + \
		fields_docpack
