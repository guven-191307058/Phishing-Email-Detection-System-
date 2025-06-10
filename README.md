(English Version)
                                                                     PHISHING DETECTION SYSTEM
📌 Project Description

✔️ This project is a machine learning-based system designed to automatically detect whether an email is a phishing attempt or a legitimate message by analyzing its content. The primary goal is to enhance email       security and protect users against phishing and identity theft attacks.


🎯 Objective

✔️ The goal is to analyze the content and specific features of incoming emails in order to detect malicious emails, particularly those intended to steal sensitive information from the user.


🚀 Key Features

✉️ Binary classification – Emails are labeled as either phishing or normal.
🧠 Advanced feature engineering – Various criteria such as email content, links, sender information, and spelling errors are analyzed.
⏰ Scheduled periodic checks – The system regularly connects to the email server via IMAP using the schedule library to fetch and analyze new emails at set intervals.
📈 High accuracy – The XGBoost-based model provides strong performance.
🔐 Data security – Sensitive information such as passwords is securely stored in a .env file.


🧠 How It Works

📍 Scheduled Email Retrieval:

✔️ The system uses the schedule library to run periodic tasks at predefined intervals. At each scheduled run, it connects to the email server via the IMAP protocol to fetch new incoming emails. This ensures continuous monitoring without manual intervention and helps the model stay up to date with fresh data.

📍 Email Fetching and Parsing:

✔️ Using Python’s imaplib and email libraries (or a custom module like email_fetcher), the raw emails are retrieved and parsed. The email body content is extracted, including handling both plain text and HTML formats.

📍 Preprocessing:

✔️ The raw email content undergoes preprocessing steps:

   ⭐ HTML Cleaning: The BeautifulSoup library is employed to strip HTML tags and convert content into plain text.

   ⭐ Spelling Correction: The SpellChecker library checks and calculates the rate of spelling errors in the email text, which is an important feature for phishing detection.

   ⭐ Removing Unwanted Characters: Regular expressions (re module) help to remove unnecessary characters and patterns like multiple spaces, special symbols, or encoded content.

📍 Feature Extraction:

✔️ Multiple features are extracted from the preprocessed emails to feed into the model:

   ⭐ URL Counting: The number of URLs and shortened URLs (e.g., bit.ly, tinyurl) are counted using regex pattern matching.

   ⭐ Phishing Keyword Frequency: The content is scanned for the presence of common phishing-related keywords from a predefined list.

   ⭐ Sender Domain Analysis: The sender’s email address is parsed to extract the domain, which is encoded numerically.

   ⭐ Spelling Error Ratio: Calculated using the SpellChecker to gauge the proportion of misspelled words.

📍 Vectorization:

✔️ The email text is transformed into numerical vectors using the TfidfVectorizer from scikit-learn. This converts text data into a format suitable for machine learning by emphasizing important words while reducing the weight of common words.

📍 Model Prediction:

✔️ An XGBoost (xgboost library) classifier is trained with these features to predict whether an email is phishing or normal. The model outputs a label for each email based on the learned patterns.

📍 Result Storage:

✔️ The predicted labels along with relevant email data are saved into a CSV file using pandas. This file serves as a log for further analysis or reporting.


🧩 Technologies Used

⭐ Python (Pandas, NumPy)
⭐ XGBoost
⭐ Scikit-learn
⭐ Natural Language Processing (NLP)
⭐ IMAPClient (email access)
⭐ dotenv (for managing sensitive information)


🔐 Security Note

✔️ This system has been developed for research and educational purposes. It is not intended to replace commercial products but provides a strong foundation for prototyping and cybersecurity research. Please keep in mind that the development is still ongoing, so use it accordingly.


📬 Contact

✔️ If you have any suggestions, feedback, or would like to contribute, please feel free to contact me at: gvnkzc847@gmail.com . Your input is highly appreciated as it helps me improve the project and better support the community.


                                                               OLTALAMA SALDIRISI TESPİT SİSTEMİ
(Türkçe Versiyonu)

📌 Proje Tanımı

✔️ Bu proje, e-posta içeriklerini analiz ederek bir e-postanın oltalama (phishing) saldırısı mı yoksa meşru bir mesaj mı olduğunu otomatik olarak tespit eden makine öğrenmesi tabanlı bir sistemdir. Temel amacı, e-posta güvenliğini artırmak ve kullanıcıları kimlik avı ve veri hırsızlığı girişimlerine karşı korumaktır.

🎯 Amaç

✔️ Gelen e-postaların içeriklerini ve belirli özelliklerini analiz ederek, özellikle kullanıcının hassas bilgilerini çalmaya yönelik kötü niyetli e-postaları tespit etmektir.

🚀 Temel Özellikler

✉️ İkili sınıflandırma – E-postalar phishing veya normal olarak etiketlenir.
🧠 Gelişmiş özellik mühendisliği – E-posta içeriği, bağlantılar, gönderici bilgisi ve yazım hataları gibi çeşitli kriterler analiz edilir.
⏰ Planlı periyodik kontrol – Sistem, schedule kütüphanesi ile belirli aralıklarla IMAP üzerinden e-posta sunucusuna bağlanarak yeni e-postaları düzenli şekilde çeker ve analiz eder.
📈 Yüksek doğruluk – XGBoost tabanlı model güçlü bir performans sunar.
🔐 Veri güvenliği – Parola gibi hassas bilgiler .env dosyasında güvenli şekilde saklanır.

🧠 Nasıl Çalışır?

📍 Planlı E-posta Çekme:
✔️ Sistem, schedule kütüphanesi kullanarak önceden tanımlanmış aralıklarla görevler çalıştırır. Her çalıştırmada IMAP protokolü ile e-posta sunucusuna bağlanarak gelen yeni e-postalar alınır. Bu sayede manuel müdahale olmadan sürekli takip sağlanır ve model güncel veriyle beslenir.

📍 E-posta Alma ve Ayrıştırma:
✔️ Python’un imaplib ve email kütüphaneleri (ya da email_fetcher gibi özel modüller) kullanılarak ham e-postalar alınır ve içerikleri ayrıştırılır. E-posta gövdesi, düz metin ve HTML formatları da dahil olmak üzere çıkarılır.

📍 Ön İşleme:
✔️ Ham e-posta içeriği şu adımlardan geçirilir:

⭐ HTML Temizleme: BeautifulSoup kütüphanesi ile HTML etiketleri kaldırılarak içerik düz metne dönüştürülür.

⭐ Yazım Düzeltme: SpellChecker kütüphanesi ile yazım hataları tespit edilir ve hata oranı hesaplanır, bu phishing tespiti için önemli bir özelliktir.

⭐ İstenmeyen Karakterlerin Kaldırılması: re (regular expressions) modülü ile gereksiz boşluklar, özel karakterler ve kodlanmış içerikler temizlenir.

📍 Özellik Çıkarımı:
✔️ İşlenmiş e-postalardan model için çeşitli özellikler çıkarılır:

⭐ URL Sayımı: Regex ile URL ve kısa linklerin (bit.ly, tinyurl vb.) sayısı bulunur.

⭐ Phishing Anahtar Kelimeler: Önceden belirlenmiş oltalama ile ilgili anahtar kelimeler aranır ve yoğunlukları hesaplanır.

⭐ Gönderen Domain Analizi: Gönderen e-posta adresinin domain kısmı çıkarılır ve sayısal olarak kodlanır.

⭐ Yazım Hatası Oranı: SpellChecker ile bulunan yazım hatalarının oranı hesaplanır.

📍 Vektörleştirme:
✔️ E-posta metni, scikit-learn’den TfidfVectorizer kullanılarak sayısal vektörlere dönüştürülür. Bu yöntem önemli kelimelerin ağırlığını artırıp yaygın kelimeleri azaltarak makine öğrenmesi için uygun format oluşturur.

📍 Model Tahmini:
✔️ XGBoost sınıflandırıcısı, bu özelliklerle eğitilmiştir ve bir e-postanın phishing mi yoksa normal mi olduğunu tahmin eder. Model öğrendiği kalıplara göre her e-postaya etiket atar.

📍 Sonuçların Kaydedilmesi:
✔️ Tahmin edilen etiketler ve ilgili e-posta verileri pandas kütüphanesi kullanılarak CSV dosyasına kaydedilir. Bu dosya ileride analiz ve raporlama için kullanılır.

🧩 Kullanılan Teknolojiler

⭐ Python (Pandas, NumPy)
⭐ XGBoost
⭐ Scikit-learn
⭐ Doğal Dil İşleme (NLP)
⭐ IMAPClient (e-posta erişimi)
⭐ dotenv (hassas bilgilerin yönetimi için)

🔐 Güvenlik Notu

✔️ Bu sistem araştırma ve eğitim amaçlı geliştirilmiştir. Ticari ürünlerin yerine geçmesi amaçlanmamıştır ancak prototipleme ve siber güvenlik araştırmaları için sağlam bir temel sunar. Geliştirme süreci halen devam ettiğinden, kullanırken dikkatli olunması tavsiye edilir.

📬 İletişim

✔️ Projeye dair öneri, geri bildirim veya katkılarınız için benimle iletişime geçmekten çekinmeyin: gvnkzc847@gmail.com. Geri bildirimleriniz projenin gelişimine katkıda bulunacak ve topluluğa daha iyi destek olmamı sağlayacaktır.
