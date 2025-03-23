from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from zlapi import Message, ThreadType, Mention, MessageStyle, MultiMsgStyle
from concurrent.futures import ThreadPoolExecutor
import time
from time import sleep 
from datetime import datetime
import threading
import random 
import json
import requests
from Crypto.Cipher import AES
import base64
import logging
def Tcp_Focx():
    try:
        with open('admin.json', 'r') as adminvip:
            adminzalo = json.load(adminvip)
            return set(adminzalo.get('idadmin', []))
    except FileNotFoundError:
        return set()
idadmin = Tcp_Focx()
class QuynhAnh(ZaloAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spamming = False
        self.spam_thread = None
        self.spammingvip = False
        self.spam_threadvip = None
        self.reo_spamming = False
        self.reo_spam_thread = None
        self.idnguoidung = ['207754413506549669']
        self.excluded_user_ids = []
        self.thread_pool = ThreadPoolExecutor(max_workers=100000000)
        self.imei = kwargs.get('imei')
        self.session_cookies = kwargs.get('session_cookies')
        self.secret_key = self.getSecretKey()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "origin": "https://chat.zalo.me",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "Accept-Encoding": "gzip",
            "referer": "https://chat.zalo.me/",
            "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        }
    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        try:
            content = message_object.content if message_object and hasattr(message_object, 'content') else ""
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except json.JSONDecodeError:
                    pass
            if isinstance(content, dict):
                action = content.get('action')
                params = content.get('params')
                if action == 'recommened.user' and params:
                    reply_id = str(params)
                    reply_message = Message(text=reply_id)
                    self.replyMessage(
                        reply_message,
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )  
                    return
            if not isinstance(message, str):
                return
        except Exception as content_error:
            logging.warning(f"Lỗi trong onMessage: {content_error}")
        if not isinstance(message, str):
            print(f"{type(message)}")
            return
        if message.startswith("Menu"):
           self.replyMessage(Message(text='''
> ├> ʙᴏᴛ ᴠɪᴘ ᴏꜰꜰ ᴅᴜᴏɴɢ ɴɢᴏᴄ ᴄᴏᴅᴇʀ
> ├ ᴀʟʟ: ᴛᴀɢ ᴀʟʟ ᴛᴇxᴛ ɴᴏ ᴋᴇʏ
> ├ ᴏꜰꜰ: ʙᴏᴛ ꜱᴛᴏᴘ ᴡᴏʀᴋɪɴɢ 
> ├ ʀᴇᴏꜱᴘ: ꜱᴘᴀᴍ ᴛᴀɢ ᴍᴇᴍʙᴇʀ 
> ├ ꜱᴛᴏᴘʀ: ꜱᴛᴏᴘ ᴛᴀɢ ꜱᴘᴀᴍ
> ├> ᴏᴛʜᴇʀꜱ ꜰᴜɴᴄᴛɪᴏɴꜱ ᴏꜰ ʙᴏᴛ
> ├ ɪɴꜰᴏ: ᴘʀᴏꜰɪʟᴇ ᴜɪᴅ ᴜꜱᴇʀ - ᴜɪᴅ ɢʀᴏᴜᴘ - ɴᴀᴍᴇ ᴜꜱᴇʀ
> ├ ꜱᴘᴀᴍ: ꜱᴘᴀᴍ ᴍᴇꜱꜱᴀɢᴇ 
> ├ ꜱᴛᴏᴘꜱᴘᴀᴍ: ꜱᴛᴏᴘ ꜱᴘᴀᴍ ᴍᴇꜱꜱᴀɢᴇ 
> ├> ʙᴏᴛ ᴢᴀʟᴏ - ᴅᴜᴏɴɢ ɴɢᴏᴄ
            '''), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("ReoSp"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return

            if self.reo_spamming:
                  self.replyMessage(Message(text='𝙎𝙪𝙘𝙘𝙚𝙨𝙨 𝙁𝙪𝙡𝙡𝙮 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                  return

            mentions = message_object.mentions
            if not mentions:
                  self.replyMessage(Message(text='🚫 𝙐𝙨𝙚 𝙍𝙚𝙤 @𝙐𝙨𝙚𝙧.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                  return

            mentioned_user_id = mentions[0]['uid']

            self.reo_spamming = True
            self.reo_spam_thread = threading.Thread(target=self.reo_spam_message, args=(mentioned_user_id, thread_id, thread_type))
            self.reo_spam_thread.start()  
        elif message.startswith("StopR"):
          with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
          if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
          if not self.reo_spamming:
                  self.replyMessage(Message(text='🚫 𝙉𝙤𝙩 𝙎𝙥𝙖𝙢 𝙍𝙚𝙤 𝙍𝙪𝙣𝙣𝙞𝙣𝙜'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                  return
          self.reo_spamming = False
          if self.reo_spam_thread is not None:
            self.reo_spam_thread.join()
            self.replyMessage(Message(text='𝙎𝙩𝙤𝙥 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Info"):
            user_id = None
            if message_object.mentions:
                user_id = message_object.mentions[0]['uid']
            elif content[5:].strip().isnumeric():
                user_id = content[5:].strip()
            else:
                user_id = author_id
            user_info = self.fetchUserInfo(user_id)
            infozalo = self.checkinfo(user_id, user_info, thread_id)
            self.replyMessage(Message(text=infozalo, parse_mode="HTML"), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("Spam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            args = content.split()
            if len(args) >= 3:
                message = " ".join(args[1:-1])
                try:
                    delay = float(args[-1])
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 𝙃𝙤𝙬 𝙏𝙤 𝘿𝙚𝙡𝙖𝙮 ?'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                        return
                    self.chayspam(message, delay, thread_id, thread_type)
                except ValueError:
                    self.replyMessage(Message(text='🚫 𝙋𝙡𝙚𝙖𝙨𝙚 𝙄𝙣𝙥𝙪𝙩 𝘿𝙚𝙡𝙖𝙮'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
            else:
                self.replyMessage(Message(text='🚫 𝙐𝙨𝙚:\n𝙎𝙥𝙖𝙢 𝙏𝙚𝙭𝙩 𝘿𝙚𝙡𝙖𝙮\n\n𝑺𝒑𝒂𝒎 𝑵𝒈𝒐𝒄 𝟓'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("StopSpam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            self.dungspam()
            self.replyMessage(Message(text='𝙎𝙩𝙤𝙥 𝙎𝙥𝙖𝙢 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Off"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            self.replyMessage(Message(text='𝙊𝙛𝙛 ! - 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 𝙁𝙪𝙡𝙡'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
            exit()
        elif message.startswith("All"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(
                Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'),
                message_object, thread_id=thread_id, thread_type=thread_type,
                ttl=30000
                )
                return
            message_content = message[4:].strip() 
            if not message_content:
                self.replyMessage(
                    Message(text="🚫 𝑷𝒍𝒆𝒂𝒔𝒆 𝑰𝒏𝒑𝒖𝒕 𝑻𝒆𝒙𝒕 𝑭𝒐𝒓 𝑨𝒍𝒍 !"),
                    message_object, thread_id=thread_id, thread_type=thread_type,
                    ttl=30000
                )
                return
            mention = Mention(uid='-1', offset=0, length=len(message_content))
            message_obj = Message(text=message_content, mention=mention)
            self.send(message_obj, thread_id=thread_id, thread_type=thread_type)
    def QuynhAnhXinh(self, thread_id, user_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']
        return user_id in admin_ids or user_id == creator_id
    def spam_message(self, spam_content, thread_id, thread_type):
        """Spam the content from content.txt file in the thread."""
        words = spam_content.split()
        while self.spamming:
            for word in words:
                if not self.spamming:
                    break
                mention = Mention(uid='-1', offset=0, length=len(word))
                spam_message = Message(text=word, mention=mention)
                self.send(spam_message, thread_id=thread_id, thread_type=thread_type)
                time.sleep(0.5)

    def reo_spam_message(self, mentioned_user_id, thread_id, thread_type):
        """Spam mentions of a specific user."""
        while self.reo_spamming:
            mention = Mention(uid=mentioned_user_id, offset=0, length=5)
            spam_message = Message(text="@user", mention=mention)
            self.send(spam_message, thread_id=thread_id, thread_type=thread_type, ttl=1000)
            time.sleep(0)
    def chayspam(self, message, delay, thread_id, thread_type):
        if self.spamming:
            self.dungspam()
        self.spamming = True
        self.spam_thread = threading.Thread(target=self.spamtagall, args=(message, delay, thread_id, thread_type))
        self.spam_thread.start()
    def dungspam(self):
        if self.spamming:
            self.spamming = False
            if self.spam_thread is not None:
                self.spam_thread.join()
            self.spam_thread = None
    def checkinfo(self, user_id, user_info, thread_id):
        if 'changed_profiles' in user_info and user_id in user_info['changed_profiles']:
            profile = user_info['changed_profiles'][user_id]
            infozalo = f'''
> ┌─────────────────────
> ├> <b>ɴᴀᴍᴇ: </b> {profile.get('displayName', '')}
> ├> <b>ɪᴅ-ᴜꜱᴇʀ: </b> {profile.get('userId', '')}
> ├> <b>ɪᴅ-ɢʀᴏᴜᴘ: </b> {thread_id}
> └─────────────────────
        '''
            return infozalo
        else:
            return "Thông tin không tồn tại."
    
client = QuynhAnh(
    '</>', '</>',
    imei="Nhập Imei",
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    session_cookies=Nhập Season Cookie)
client.listen()