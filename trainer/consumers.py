import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
class JobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.job_group_name = f'job_{self.job_id}'

        print(f"✅ WebSocket BAĞLANTISI KURULDU: {self.job_group_name} grubuna.")

        await self.channel_layer.group_add(
            self.job_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f"❌ WebSocket BAĞLANTISI KESİLDİ: {self.job_group_name} grubundan.")
        await self.channel_layer.group_discard(
            self.job_group_name,
            self.channel_name
        )

    async def job_update(self, event):
     
        from .models import TrainingJob


        print(f"📢 GRUP MESAJI ALINDI: {self.job_group_name} için güncelleme.")
        job_id = event['job_id']
        job = await TrainingJob.objects.aget(id=job_id)
        html = render_to_string('trainer/_job_status_partial.html', {'job': job})
        print("🚀 HTML GÖNDERİLİYOR...")
        await self.send(text_data=html)