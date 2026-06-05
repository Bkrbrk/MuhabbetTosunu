import discord
from discord.ext import commands, tasks
import random
import time
import json
from keep_alive import keep_alive

# Gerekli ID'ler ve Token
TOKEN = 'MTUxMjUyNzU2NjQyOTM2MDM0MA.GCkvRw.qwJa78vv5NMRbUTkRjg1FOdiCMyxE6QmG0dYMI'
HEDEF_KANAL_ID = 1512531847207194866 # Kanala sağ tıklayıp "ID'yi Kopyala" de
PING_ROL_ID = 1512532272207626250 # Etiketlenecek role sağ tıklayıp "ID'yi Kopyala" de

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Zamanlayıcı ve Soru Havuzu Değişkenleri
son_mesaj_zamani = time.time()
# 2 saat (7200 sn) ile 4 saat (14400 sn) arası rastgele bir süre seçen fonksiyon
def rastgele_sure_sec():
    return random.randint(7200, 14400)

BEKLEME_SURESI = rastgele_sure_sec()

tum_sorular = []
kalan_sorular = []

# JSON dosyasından soruları güvenli bir şekilde yükleyen fonksiyon
def sorulari_yukle():
    global tum_sorular, kalan_sorular
    try:
        with open('sorular.json', 'r', encoding='utf-8') as f:
            tum_sorular = json.load(f)
            kalan_sorular = tum_sorular.copy() # Soruları korumak için kopyasını oluşturuyoruz
            print(f"Başarıyla {len(tum_sorular)} adet soru havuzdan yüklendi!")
    except FileNotFoundError:
        print("HATA: 'sorular.json' dosyası bulunamadı! Lütfen dosyanın adını kontrol edin.")
    except json.JSONDecodeError:
        print("HATA: 'sorular.json' dosyasının formatı hatalı! Virgülleri veya tırnakları kontrol edin.")

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')
    sorulari_yukle() # Bot açılırken soruları yükle
    zaman_kontrol_dongusu.start()

@bot.event
async def on_message(message):
    global son_mesaj_zamani
    
    if message.author == bot.user:
        return

    if message.channel.id == HEDEF_KANAL_ID:
        son_mesaj_zamani = time.time()
        print("Yeni bir mesaj geldi, kronometre sıfırlandı.")

    await bot.process_commands(message)

@tasks.loop(seconds=10) # Döngü her 10 saniyede bir kontrol etmeye devam etsin
async def zaman_kontrol_dongusu():
    global son_mesaj_zamani, kalan_sorular, BEKLEME_SURESI
    
    su_an = time.time()
    gecen_sure = su_an - son_mesaj_zamani
    
    if gecen_sure >= BEKLEME_SURESI:
        kanal = bot.get_channel(HEDEF_KANAL_ID)
        
        if not kalan_sorular:
            print("Havuzdaki tüm sorular bitti. Yenileniyor...")
            kalan_sorular = tum_sorular.copy()
            
        secilen_soru = random.choice(kalan_sorular)
        kalan_sorular.remove(secilen_soru)
        
        mesaj_metni = f"<@&{PING_ROL_ID}> Ortam biraz sessizleşmiş... Gelin biraz beyin fırtınası yapalım!\n\n**{secilen_soru}**\n\n*(Lütfen birbirimizin fikirlerine saygı göstererek tartışalım 💡)*"
        
        await kanal.send(mesaj_metni)
        
        # Soru sorulduktan sonra kronometreyi sıfırla ve YENİ BİR RASTGELE SÜRE belirle
        son_mesaj_zamani = time.time()
        BEKLEME_SURESI = rastgele_sure_sec()
# Web sunucusunu ve botu başlat
keep_alive()
bot.run(TOKEN)