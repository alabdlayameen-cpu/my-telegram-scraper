import os
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError

# --- أدخل بياناتك البرمجية هنا ---
API_ID = 1234567       # استبدل هذا الرقم بـ App api_id الخاص بك
API_HASH = abcdef1234567890abcdef1234567890  # استبدل هذا النص بـ App api_hash الخاص بك
# ---------------------------------

client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    await client.start()
    print("تم تسجيل الدخول بنجاح إلى تليجرام!")
    
    # 1. جلب المجموعات المشترك بها
    dialogs = await client.get_dialogs()
    groups = [d for d in dialogs if d.is_group]
    
    print("\n--- المجموعات المتاحة في حسابك ---")
    for i, g in enumerate(groups):
        print(f"[{i}] - {g.name}")
        
    source_index = int(input("\nأدخل رقم المجموعة التي تريد (سحب) الأعضاء منها: "))
    target_index = int(input("أدخل رقم مجموعتك التي تريد (إضافة) الأعضاء إليها: "))
    
    source_group = groups[source_index]
    target_group = groups[target_index]
    
    print(f"\nجاري سحب الأعضاء من: {source_group.name}...")
    all_participants = await client.get_participants(source_group)
    print(f"تم العثور على {len(all_participants)} عضو.")
    
    # 2. بدء إضافة الأعضاء تلقائياً
    print(f"\nبدء إضافة الأعضاء إلى مجموعتك: {target_group.name}...")
    
    for user in all_participants:
        if user.bot or user.deleted:
            continue
            
        try:
            # محاولة إضافة العضو باستخدام معرفه الرقمي
            await client(InviteToChannelRequest(target_group, [user]))
            print(f"✅ تم إضافة العضو بنجاح: {user.first_name or user.username}")
            # وقت انتظار بين كل إضافة لحماية الحساب من الحظر الفوري (Spam)
            time.sleep(15) 
            
        except PeerFloodError:
            print("⚠️ تحذير: حسابك واجه قيود السحب (Flood Error) من تليجرام. سيتم إيقاف السكريبت مؤقتاً.")
            time.sleep(300) # الانتظار 5 دقائق في حال ضغط السيرفر
        except UserPrivacyRestrictedError:
            print(f"❌ تعذر إضافة {user.first_name} بسبب إعدادات الخصوصية الخاصة به.")
        except Exception as e:
            print(f"❌ خطأ غير متوقع مع العضو {user.id}: {e}")

with client:
    client.loop.run_until_complete(main())
