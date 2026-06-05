# MuhabbetTosunu - Discord Etkileşim Botu

MuhabbetTosunu, Discord sunucularındaki sessizliği bozmak ve insanları yeniden sohbete dahil etmek için geliştirilmiş bir etkileşim botudur. Sohbetin durakladığı anları tespit eder ve rastgele aralıklarla ucu açık, tartışmaya teşvik eden sorular sorarak topluluğu canlı tutar.

## Özellikler

* **Dinamik Zamanlayıcı:** Soruları belirli bir rutinde değil, 2 ile 4 saat arasında rastgele belirlenen sürelerde (7200 - 14400 saniye) sorarak yapay hissiyatı ortadan kaldırır.
* **Akıllı Sıfırlama:** Hedef kanala bir kullanıcı tarafından mesaj atıldığında sayacı otomatik olarak sıfırlar. Sadece sohbet gerçekten öldüğünde devreye girer.
* **Geniş Soru Havuzu:** Harici bir `sorular.json` dosyasından beslenir. Sorulan bir soruyu havuz bitene kadar tekrar sormaz.
* **Hedefli Bildirim:** Soruyu sorarken sadece belirlenen özel role (Örn: `@SoruCevap`) ping atarak sunucudaki diğer üyeleri rahatsız etmez.
* **7/24 Uyku Koruması:** Render ve benzeri ücretsiz bulut platformlarında uyku moduna geçmesini engellemek için arka planda hafif bir `Flask` web sunucusu çalıştırır.

## Kullanılan Teknolojiler

* **Python 3**
* **discord.py** (Discord API entegrasyonu)
* **Flask** (Keep-alive workaround sunucusu)
* **JSON** (Veri ve soru havuzu yönetimi)

## Nasıl Çalışır?

1. Bot ayağa kalktığında `sorular.json` dosyasındaki soruları hafızasına alır.
2. Arka planda geri sayım başlar (Rastgele 2-4 saat).
3. Süre dolduğunda havuzdan rastgele bir soru çeker, belirlediğiniz role ping atarak soruyu kanala gönderir.
4. Sorulan soruyu geçici olarak listeden çıkarır ve bir sonraki soru için yeni bir rastgele süre belirleyip beklemeye geçer.
