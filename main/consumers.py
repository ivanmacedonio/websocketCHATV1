import json 
from channels.generic.websocket import AsyncWebsocketConsumer #importamos el consumer asincrono

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self): #establece la conexion entre el cliente y servidor
        
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]   
        self.group_name= "chat_%s" % self.chat_box_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        #indicamos que canal eliminar de que grupo

    async def receive(self,text_data): #recibimos mensaje, lo desglozamos y muestra en el grupo
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        await self.channel_layer.group_send( #le indicamos nombre del grupo y la info que envia 
            self.group_name,{
                "type":"chatbox_message",
                "message": message,
                "username": username,
            },
        )

    async def chatbox_message(self,event): #el servidor retorna el mensaje del canal al grupo
        message = event["message"]
        username = event["username"]
        await self.send(
            text_data=json.dumps(
            {
                "message":message,
                "username": username,
            }
            )
        )
    pass






