# 编写处理websocket的业务逻辑
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """ 有客户端向后端发送websocket连接的请求时，自动触发 """
        print(">>> 有人来连接了 <<<")
        # 接收客户端连接，服务端允许和客户端创建连接--握手
        self.accept()

        # 获取组号
        group = self.scope['url_route']['kwargs'].get('group')

        # 将客户端的连接对象加入到某个地方（内存 or redis）
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

        # 服务端主动给客户端发送消息
        # self.send("欢迎进群！")

    def websocket_receive(self, message):
        """ 浏览器基于websocket向后端发送数据，自动触发接收消息 """
        # print( message)
        text = message["text"]
        print("接收到消息-->", text)
        if text == "close":
            # 服务端主动关闭连接，给客户端发送一条断开连接的消息
            self.close()
            # raise StopConsumer()  # 若在这里执行stopconsumer异常，那么websocket_disconnect方法不再执行
            return  # websocket_disconnect会执行
        res = "{}--CHAT".format(text)

        group = self.scope['url_route']['kwargs'].get('group')
        #  通知组内的所有客户端，执行 aabb 的方法，在此方法中可以自定义任意功能
        async_to_sync(self.channel_layer.group_send)(group, {"type": "aabb", "message": message})

        # self.send(res)  # 给当前这一个连接回复

    def aabb(self, event):
        text = event["message"]["text"]
        self.send(text)  # 给组内的每一个连接回复

    def websocket_disconnect(self, message):
        """ 客户端与服务端断开连接时，自动触发 """
        print(">>> 客户端主动请求断开连接 <<<")
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer()