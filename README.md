# python-Chatroom

This is to implement Chatroom App through Python's SCOKET library
## Protocol design
Before starting to write a program, the design of the protocol is extremely important. At present we are going to learn the TCP/IP protocol and make some appropriate changes on this basis to make it more suitable for our APP
```
||user|type|num|data|recvnamelist||
||发送者|类型|包的数量1024Byte 24B  001/005|数据||

类型 --》文本消息 mesg
 	--》文件传输 //内置文件格式表   filetype 读取文件格式
 		--》txt
 		--》图片
 	

接收者--》单播/单发
     --》组播
     	--》先发接收者列表  //第一个包
     	--》再发数据包
     
```


## Basic Functions goal

- [ ] Login and registration functions

Implement basic chat functions

- [ ] Add user
- [ ] Add group

- [ ] Send text message
- [ ] Send File
- [ ] send the pictures & videos
- [ ] Send voice message
- [ ] more...

## Encrypted chat

Concealment in the chat process is extremely important, so the design of an encrypted chat protocol is also extremely important.

- [ ] Symmetric encryption
- [ ] Asymmetric encryption
