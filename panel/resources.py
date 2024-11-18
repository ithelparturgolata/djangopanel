from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Smieci, Budynek


class SmieciResource(resources.ModelResource):
	budynek = fields.Field(
		column_name='budynek',
		attribute='budynek',
		widget=ForeignKeyWidget(Budynek, 'indeks')
	)
	
	styczen = fields.Field(attribute='styczen', column_name='styczen')
	luty = fields.Field(attribute='luty', column_name='luty')
	marzec = fields.Field(attribute='marzec', column_name='marzec')
	kwiecien = fields.Field(attribute='kwiecien', column_name='kwiecien')
	maj = fields.Field(attribute='maj', column_name='maj')
	czerwiec = fields.Field(attribute='czerwiec', column_name='czerwiec')
	lipiec = fields.Field(attribute='lipiec', column_name='lipiec')
	sierpien = fields.Field(attribute='sierpien', column_name='sierpien')
	wrzesien = fields.Field(attribute='wrzesien', column_name='wrzesien')
	pazdziernik = fields.Field(attribute='pazdziernik', column_name='pazdziernik')
	listopad = fields.Field(attribute='listopad', column_name='listopad')
	grudzien = fields.Field(attribute='grudzien', column_name='grudzien')
	
	class Meta:
		model = Smieci
		fields = ('budynek', 'styczen', 'luty', 'marzec', 'kwiecien', 'maj', 'czerwiec',
				  'lipiec', 'sierpien', 'wrzesien', 'pazdziernik', 'listopad', 'grudzien')
		import_id_fields = ['budynek']

