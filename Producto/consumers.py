import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Inventario.models import Inventario
from Bodega.models import Bodegas
from django.db.models import DecimalField, F, ExpressionWrapper

class ComponentesDisponiblesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            id_componente = data.get('id_componente')
            cantxensamble = Decimal(data.get('cantxensamble'))
            catngenensamble = Decimal(data.get('catngenensamble'))
            id_componentegen = data.get('id_componentegen')
            cantxfabricar = Decimal(data.get('cantxfabricar'))
            id_bodega = Bodegas.objects.get(id_bodega=data.get('id_bodega'))

            componentepadre = Componente.objects.get(id_componente=id_componentegen)
            componentehijo = Componente.objects.get(id_componente=id_componente)
            ensamble = EnsambleComponente.objects.get(id_componentepadre=componentepadre)
            detalle = DetalleEnsambleComponente.objects.filter(id_ensamblec=ensamble, id_componentehijo=componentehijo)

            cantnecesaria = ExpressionWrapper(F('cantxensamble') * F('cantxfabricar') / F('catngenensamble'), output_field=DecimalField())

            inventario = Inventario.objects.get(id_componente=componentehijo, id_bodega=id_bodega)
            print(cantnecesaria)
            print('<=')
            print(float(inventario.cantidad_disponible))
            if float(cantnecesaria) <= float(inventario.cantidad_disponible):
                print(1)
                await self.send(text_data=json.dumps({'mensaje': 1}))
            else:
                print('Cantidad de fabricar: ' + data.get('cantxfabricar'))
                print(0)
                await self.send(text_data=json.dumps({'mensaje': 0}))

        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))
