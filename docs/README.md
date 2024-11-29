
# Luxoft Hackathon Case Çözümü (ALİ ÖZEN)

Bu proje, Luxoft Hackathon'unda verilen bir problemi çözmek için geliştirilmiş algoritmaları ve çözüm yaklaşımlarını içerir. Proje, hem ana çözümü hem de alternatif algoritmaların performans karşılaştırmasını ele almaktadır.

## Proje Yapısı

```
Luxoft_Hackathon_Case_Cozumu/
├── src/
│   ├── algorithm_comparison.py   # Algoritma karşılaştırması için (BFS, Dijkstra, A* gibi)
│   ├── solution.py               # Ana çözüm dosyası
│   
├── tests/
│   ├── scenarios.txt             # Ana çözüm için kullanılan senaryolar
│   ├── test_scenarios_for_comparison.txt  # Algoritma karşılaştırmaları için test verileri
├── docs/
│   └── README.md                 # Proje açıklamaları
├── requirements.txt              # Gerekli bağımlılıkların listesi
```

## Özellikler

- **Ana Çözüm**:
  - Senaryolarda verilen problemleri çözmek için BFS ile  çözüm algoritması içerir.
  - Çözüm, girdilere dayalı olarak doğru çıktılar üretir.
  - Girdiler tkinter ile yapılmış arayüz ile başlangıç noktasıdır.
  - Başlangıç noktasını aldıktan sonra BFS algoritması çalışır en uygun yeri belirler ve gittiği yolu matplotlib ile çizerek görselleştirir.
  - Başka senaryo denemek için arayüz kullanılabilir. Txt dosyasında olan senaryolar arayüz ile görülebilmektedir bu sayede istenilen senaryo rahatlıkla seçilebilir.

- **Algoritma Karşılaştırma**:
  - BFS, Dijkstra ve A* gibi algoritmaların hız ve doğruluk karşılaştırmalarını yapar.
  - Her algoritmanın senoryalardaki performansını ölçer.
  - Matplotlib ile görseleştirerek en uygun algoritmayı seçmede yardımcı olur

- **Senaryo Yönetimi**:
  - `scenarios.txt` ve `test_scenarios_for_comparison.txt` dosyalarını kullanarak senaryoları işler.
  - Modüler yapısı sayesinde farklı veri setleri kolayca entegre edilebilir.

## Kullanım

### Gerekli Bağımlılıklar
Projeyi çalıştırmadan önce aşağıdaki bağımlılıkların yüklü olduğundan emin olun. Bağımlılıkları yüklemek için aşağıdaki komutu kullanabilirsiniz:

```bash
pip install -r requirements.txt
```

### Çalıştırma

#### Ana Çözümü Çalıştırmak İçin
```bash
cd src
python3 solution.py
```

#### Algoritma Karşılaştırmayı Çalıştırmak İçin
```bash
cd src
python3 algorithm_comparison.py
```

### Veri Dosyalarını Düzenleme
- **`scenarios.txt`**: Ana çözüm için gerekli senaryolar.
- **`test_scenarios_for_comparison.txt`**: Algoritma karşılaştırma için test verileri.

Her dosya, aşağıdaki formatta düzenlenmelidir:

**Senaryo Formatı**:
```plaintext
# Senaryo Adı
5                     # Grid boyutu
0 0 0 0 0             # Grid verileri
0 1 1 1 0
0 1 0 1 0
0 1 1 1 0
0 0 0 0 0
---                   # Birden fazla senaryo için ayırıcı
```

**Test Senaryo Formatı**:
```plaintext
# Test 1
5                     # Grid boyutu
2 2                   # Başlangıç pozisyonu
1 1 1 1 1             # Grid verileri
1 0 0 0 1
1 0 1 0 1
1 0 0 0 1
1 1 1 1 1
```

## Katkıda Bulunma

Katkıda bulunmak için aşağıdaki adımları takip edebilirsiniz:
1. Projeyi fork edin.
2. Yeni bir branch oluşturun: `git checkout -b feature/ozellik-adi`.
3. Değişikliklerinizi commit edin: `git commit -m 'Yeni bir özellik eklendi'`.
4. Branch'i push edin: `git push origin feature/ozellik-adi`.
5. Bir pull request açarak değişikliklerinizi incelemeye gönderin.


