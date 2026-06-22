import discord
from discord.ext import commands, tasks
import random
import time
import json
from keep_alive import keep_alive

TOKEN = 'MTUxMjUyNzU2NjQyOTM2MDM0MA.GCkvRw.qwJa78vv5NMRbUTkRjg1FOdiCMyxE6QmG0dYMI'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 6 saat (21600 sn) ile 12 saat (43200 sn) arası
def rastgele_sure_sec():
    return random.randint(21600, 43200)

# İKİ SUNUCU İÇİN BASİT AYAR BLOKU
hedefler = {
    # 1. SUNUCU (Senin Sunucun)
    1512531847207194866: { # BURAYA KENDİ KANAL ID'Nİ YAZ
        "rol_id": 1512532272207626250, # BURAYA KENDİ ROL ID'Nİ YAZ
        "son_mesaj": time.time(),
        "kalp_atsin": True,
        "bekleme": rastgele_sure_sec()
    },
    
    # 2. SUNUCU (Arkadaşının Sunucusu)
    1499847917819793489: { # BURAYA ARKADAŞININ KANAL ID'SİNİ YAZ
        "rol_id": 1518556511901847683, # BURAYA ARKADAŞININ ROL ID'SİNİ YAZ
        "son_mesaj": time.time(),
        "kalp_atsin": False,
        "bekleme": rastgele_sure_sec()
    }
}

tum_sorular = []
kalan_sorular = []

def sorulari_yukle():
    global tum_sorular, kalan_sorular
    try:
        with open('sorular.json', 'r', encoding='utf-8') as f:
            tum_sorular = json.load(f)
            kalan_sorular = tum_sorular.copy()
    except Exception as e:
        print(f"Hata: {e}")

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı! İki sunucu dinleniyor.')
    sorulari_yukle()
    zaman_kontrol_dongusu.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    kanal_id = message.channel.id
    
    # Mesaj bizim dinlediğimiz o 2 kanaldan birine geldiyse
    if kanal_id in hedefler:
        # O kanalın kronometresini sıfırla
        hedefler[kanal_id]["son_mesaj"] = time.time()
        print(f"Mesaj geldi, {kanal_id} kanalının kronometresi sıfırlandı.")
        
        # SADECE AYARLARDA 'kalp_atsin' TRUE İSE KALP AT
        if hedefler[kanal_id].get("kalp_atsin", False):
            try:
                await message.add_reaction("❤️")
            except:
                pass

    await bot.process_commands(message)

@tasks.loop(seconds=60)
async def zaman_kontrol_dongusu():
    global kalan_sorular
    su_an = time.time()
    
    # İki kanalı da sırayla kontrol et
    for kanal_id, ayarlar in hedefler.items():
        gecen_sure = su_an - ayarlar["son_mesaj"]
        
        if gecen_sure >= ayarlar["bekleme"]:
            kanal = bot.get_channel(kanal_id)
            if kanal is None:
                continue
                
            if not kalan_sorular:
                kalan_sorular = tum_sorular.copy()
                
            secilen_soru = random.choice(kalan_sorular)
            kalan_sorular.remove(secilen_soru)
            
            mesaj_metni = f"<@&{ayarlar['rol_id']}> Ortam biraz sessizleşmiş... Gelin biraz beyin fırtınası yapalım!\n\n**{secilen_soru}**\n\n*(Lütfen birbirimizin fikirlerine saygı göstererek tartışalım 💡)*"
            
            try:
                await kanal.send(mesaj_metni)
            except:
                pass
            
            # Soru sorduktan sonra o kanalın kronometresini yeniden başlat
            ayarlar["son_mesaj"] = time.time()
            ayarlar["bekleme"] = rastgele_sure_sec()

keep_alive()
bot.run(TOKEN)
