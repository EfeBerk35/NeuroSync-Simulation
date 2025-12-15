import tkinter as tk
import math
import random

class NeuroSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroSync - Nöral Arayüz Simülasyonu (Nihai Versiyon)")
        self.root.geometry("900x600")
        self.root.configure(bg="#0a0a0a")
        
        # --- Renk Paleti (Cyberpunk/Neon) ---
        self.colors = {
            "bg": "#0a0a0a",           # Ana arka plan (Koyu Siyah)
            "panel_bg": "#111111",     # Panel içi (Az daha açık siyah)
            "accent": "#00ffcc",       # Vurgu Rengi (Neon Camgöbeği)
            "border_dim": "#333333",   # Pasif kenarlık rengi
            "text_dim": "#666666",     # Pasif metin rengi
            "warning": "#ffff00",      # İşlem rengi (Sarı)
            "success": "#00ff00",      # Başarı rengi (Yeşil)
        }
        
        # Durum bayrakları
        self.is_running = False
        self.wave_phase = 0
        
        self.setup_ui()
        
        # Uygulama açıldıktan kısa bir süre sonra senaryoyu başlat
        self.root.after(500, self.start_scenario_sequence)

    def setup_ui(self):
        # Ana Taşıyıcı Çerçeve
        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Üst Kısım Taşıyıcı (Sol ve Sağ Paneller için)
        top_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        top_frame.pack(expand=True, fill="both")
        
        # --- SOL PANEL: EEG Sinyali ---
        # Not: highlightthickness=1 ve highlightbackground kullanarak
        # dinamik olarak rengi değişebilen kenarlıklar oluşturuyoruz.
        self.left_panel = tk.LabelFrame(top_frame, text=" Canlı EEG Sinyal Akışı ", 
                                       bg=self.colors["panel_bg"], fg=self.colors["text_dim"], 
                                       font=("Courier", 10), bd=0, 
                                       highlightthickness=1, highlightbackground=self.colors["border_dim"])
        self.left_panel.pack(side="left", expand=True, fill="both", padx=5)
        
        self.canvas = tk.Canvas(self.left_panel, bg="#000000", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=5, pady=5)
        
        # --- SAĞ PANEL: AI Analizi ---
        self.right_panel = tk.LabelFrame(top_frame, text=" AI Analizi ", 
                                        bg=self.colors["panel_bg"], fg=self.colors["text_dim"],
                                        font=("Courier", 10), bd=0,
                                        highlightthickness=1, highlightbackground=self.colors["border_dim"])
        self.right_panel.pack(side="right", expand=True, fill="both", padx=5)
        
        # Durum Metni
        self.lbl_status = tk.Label(self.right_panel, text="Bekleniyor...", 
                                  bg=self.colors["panel_bg"], fg="white", 
                                  font=("Courier", 12, "bold"), pady=20)
        self.lbl_status.pack(anchor="w", padx=10)
        
        # Özel Progress Bar (Canvas ile çizim)
        self.progress_canvas = tk.Canvas(self.right_panel, height=20, bg="#222", highlightthickness=0)
        self.progress_canvas.pack(fill="x", padx=10, pady=10)
        # Başlangıçta genişliği 0 olan bir dikdörtgen
        self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 20, fill=self.colors["accent"], width=0)
        
        # Sonuçlar Alanı
        self.lbl_results = tk.Label(self.right_panel, text="", justify="left",
                                   bg=self.colors["panel_bg"], fg="#ddd",
                                   font=("Courier", 11))
        self.lbl_results.pack(anchor="w", padx=10, pady=10)

        # --- ALT PANEL: Komut Çıktısı ---
        self.bottom_panel = tk.Frame(main_frame, bg="#001a1a", bd=0, 
                                     highlightthickness=1, highlightbackground=self.colors["border_dim"])
        self.bottom_panel.pack(side="bottom", fill="x", pady=10, ipady=15)
        
        # Alt panel başlığı (Frame içinde bir Label)
        self.lbl_command_title = tk.Label(self.bottom_panel, text="[ Çözümlenen Komut ]", 
                 bg="#001a1a", fg=self.colors["text_dim"], font=("Courier", 10))
        self.lbl_command_title.pack(pady=5)
        
        # Daktilo efekti uygulanacak ana metin alanı
        self.lbl_command = tk.Label(self.bottom_panel, text="", 
                                   bg="#001a1a", fg="white", 
                                   font=("Courier", 18, "bold"))
        self.lbl_command.pack()

        # --- KATMANLAR (Overlay - Başlangıç Ekranı) ---
        self.overlay = tk.Frame(self.root, bg="black")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lift() # En üstte tut

        self.btn_start = tk.Button(self.overlay, text="SİMÜLASYONU BAŞLAT", 
                                  bg="black", fg=self.colors["accent"],
                                  font=("Courier", 16, "bold"), bd=2, relief="solid",
                                  activebackground=self.colors["accent"], activeforeground="black",
                                  padx=20, pady=10)
        self.btn_start.place(relx=0.5, rely=0.5, anchor="center")
        
        # Sahte Fare İmleci
        self.cursor = tk.Label(self.root, text="➤", bg=self.colors["bg"], fg="white", font=("Arial", 20))
        self.cursor.place(x=-50, y=-50) # Başlangıçta ekran dışına sakla

    # --- YARDIMCI FONKSİYON: Vurgulama (Highlight) ---
    def set_highlight(self, panel, active=False):
        """Bir panelin kenarlığını ve başlığını aktif/pasif durumuna göre boyar."""
        border_col = self.colors["accent"] if active else self.colors["border_dim"]
        text_col = self.colors["accent"] if active else self.colors["text_dim"]
        
        # Kenarlık rengini değiştir
        panel.config(highlightbackground=border_col, highlightcolor=border_col)
         
        # Başlık metni rengini değiştir
        if isinstance(panel, tk.LabelFrame):
            panel.config(fg=text_col)
        elif panel == self.bottom_panel:
             self.lbl_command_title.config(fg=text_col)

    # --- ANİMASYON MANTIKLARI ---
    def draw_eeg_loop(self):
        """Tuval üzerine sürekli akan sinüs dalgaları çizer."""
        if not self.is_running: return
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.delete("all") # Temizle
        
        points = []
        center_y = h / 2
        
        # Karmaşık bir dalga formu oluşturmak için sinüsleri birleştiriyoruz
        for x in range(0, w, 5):
            y = center_y + \
                math.sin((x + self.wave_phase) * 0.05) * 50 + \
                math.sin((x - self.wave_phase) * 0.1) * 20 + \
                random.uniform(-5, 5) # Gürültü ekle
            points.append(x)
            points.append(y)
            
        self.canvas.create_line(points, fill=self.colors["accent"], width=2, smooth=True)
        self.wave_phase += 5 # Dalgayı kaydır
        self.root.after(30, self.draw_eeg_loop) # 30ms sonra tekrar çağır

    def type_writer_effect(self, text, index=0):
        """Metni harf harf yazar (Daktilo efekti)."""
        if index < len(text):
            current_text = self.lbl_command.cget("text")
            self.lbl_command.config(text=current_text + text[index])
            self.root.after(80, self.type_writer_effect, text, index + 1)

    def update_progress(self, width_pct):
        """İlerleme çubuğunu animasyonla doldurur."""
        canvas_width = self.progress_canvas.winfo_width()
        current_x = (width_pct / 100) * canvas_width
        # Dikdörtgenin sağ kenarını güncelle
        self.progress_canvas.coords(self.progress_rect, 0, 0, current_x, 20)
        
        if width_pct < 100:
            self.root.after(20, self.update_progress, width_pct + 1)

    # --- SENARYO ZAMAN AKIŞI (Timeline) ---
    def start_scenario_sequence(self):
        # 0. Saniye: İmleç belirir ve harekete başlar
        self.cursor.place(x=700, y=500)
        self.cursor.lift()
        self.move_cursor_to_center(steps=20)
        
    def move_cursor_to_center(self, steps):
        """
        DÜZELTİLMİŞ FONKSİYON:
        İmleci merkeze taşır. 'steps' 0 olduğunda bölme hatası vermemesi için
        hesaplamalar 'if steps > 0' bloğu içine alınmıştır.
        """
        if steps > 0:
            # Hedef ve mevcut konum hesapla
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            target_x = w / 2
            target_y = h / 2
            
            current_x = int(self.cursor.place_info()['x'])
            current_y = int(self.cursor.place_info()['y'])
            
            # Adım başına hareket miktarı (Artık güvenli, 0'a bölünme yok)
            dx = (target_x - current_x) / steps
            dy = (target_y - current_y) / steps
            
            # Yeni konuma taşı ve bir sonraki adım için bekle
            self.cursor.place(x=current_x + dx, y=current_y + dy)
            self.root.after(40, self.move_cursor_to_center, steps - 1)
        else:
            # Hedefe (butona) varıldı
            self.simulate_click()

    def simulate_click(self):
        # 1-2 Saniye: Tıklama efekti
        self.btn_start.config(bg=self.colors["accent"], fg="black")
        self.root.after(200, self.remove_overlay)

    def remove_overlay(self):
        # Overlay'i kaldır, ana sahneye geç
        self.overlay.place_forget()
        self.cursor.place_forget()
        self.start_main_sequence()

    def start_main_sequence(self):
        # 2-6 Saniye: EEG Başlıyor -> SOL PANELİ VURGULA
        self.set_highlight(self.left_panel, active=True) 
        
        self.is_running = True
        self.draw_eeg_loop()
        self.lbl_status.config(text="Nöral sinyaller alınıyor...", fg=self.colors["accent"])
        
        # 4 saniye sonra bir sonraki adıma geç
        self.root.after(4000, self.step_processing)

    def step_processing(self):
        # 6-8 Saniye: AI İşliyor -> SAĞI VURGULA, Solu söndür
        self.set_highlight(self.left_panel, active=False)
        self.set_highlight(self.right_panel, active=True)
        
        self.lbl_status.config(text="AI modeli veriyi işliyor...", fg=self.colors["warning"])
        self.update_progress(0) # Barı doldurmaya başla
        
        # 2 saniye sonra sonuçlara geç
        self.root.after(2000, self.step_results)

    def step_results(self):
        # 8-9 Saniye: Sonuçlar aniden belirir (Vurgu sağda kalır)
        self.lbl_status.config(text="Komut çözümlendi!", fg=self.colors["success"])
        self.progress_canvas.coords(self.progress_rect, 0, 0, 0, 0) # Barı gizle/sıfırla
        
        results_text = """> Dominant Frekans: 14.2 Hz (Beta)\n> Odak Seviyesi:    %89 (Yüksek)\n> Artefakt:         Temiz"""
        self.lbl_results.config(text=results_text)
        
        # 1 saniye sonra yazmaya başla
        self.root.after(1000, self.step_typing)

    def step_typing(self):
        # 9-12 Saniye: Komut Yazılıyor -> ALTI VURGULA, Sağı söndür
        self.set_highlight(self.right_panel, active=False)
        self.set_highlight(self.bottom_panel, active=True)
        
        target_text = "Navigasyon: Eve rota oluştur."
        self.lbl_command.config(text="") # Önce temizle
        self.type_writer_effect(target_text)
        
        # 5 saniye sonra (14. saniye civarı) başa sar
        self.root.after(5000, self.reset_simulation)

    def reset_simulation(self):
        # 14. Saniye: Reset -> TÜM VURGULARI SÖNDÜR ve başa dön
        self.set_highlight(self.left_panel, active=False)
        self.set_highlight(self.right_panel, active=False)
        self.set_highlight(self.bottom_panel, active=False)
        
        # Değişkenleri ve arayüzü sıfırla
        self.is_running = False
        self.lbl_status.config(text="Bekleniyor...", fg="white")
        self.lbl_results.config(text="")
        self.lbl_command.config(text="")
        self.btn_start.config(bg="black", fg=self.colors["accent"])
        
        # Overlay'i geri getir
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lift()
        
        # Senaryoyu yeniden başlat
        self.root.after(1000, self.start_scenario_sequence)

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroSyncApp(root)
    root.mainloop()
    import tkinter as tk
from tkinter import ttk
import math
import random
import datetime

class NeuroSyncPro:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroSync PRO v2.0 - Advanced Neural Interface")
        self.root.geometry("1200x800") # Ekranı büyüttük
        self.root.configure(bg="#050505")
        
        # --- Cyberpunk Renk Paleti ---
        self.colors = {
            "bg": "#050505",
            "panel_bg": "#0f0f0f",
            "accent": "#00ffcc",    # Cyan
            "secondary": "#ff00ff", # Magenta (İkincil veri için)
            "grid": "#1a1a1a",
            "text_main": "#e0e0e0",
            "text_dim": "#555555",
            "success": "#00ff99",
            "warning": "#ffcc00",
            "danger": "#ff3333"
        }

        # Simülasyon Değişkenleri
        self.is_running = False
        self.wave_phase = 0
        self.channels = ["Frontal Lobe (Fp1)", "Parietal Lobe (P3)", "Temporal Lobe (T7)", "Occipital Lobe (O1)"]
        self.gain = 1.0 # Sinyal gücü çarpanı

        self.setup_layout()
        self.start_system_idle()

    def setup_layout(self):
        # --- ANA KONTEYNER (Izgara Sistemi) ---
        # Sol: Menü, Orta: Grafikler, Sağ: Analiz, Alt: Terminal
        
        # 1. ÜST HEADER
        header_frame = tk.Frame(self.root, bg=self.colors["panel_bg"], height=50)
        header_frame.pack(side="top", fill="x")
        tk.Label(header_frame, text="NEUROSYNC // PRO INTERFACE", 
                 bg=self.colors["panel_bg"], fg=self.colors["accent"], 
                 font=("Courier", 14, "bold")).pack(side="left", padx=20, pady=10)
        
        self.lbl_connection = tk.Label(header_frame, text="● BAĞLANTI BEKLENİYOR", 
                                      bg=self.colors["panel_bg"], fg=self.colors["danger"], font=("Arial", 9))
        self.lbl_connection.pack(side="right", padx=20)

        # 2. ALT KISIM (Terminal)
        bottom_frame = tk.Frame(self.root, bg="#000", height=150)
        bottom_frame.pack(side="bottom", fill="x")
        
        # Terminal Başlığı
        tk.Label(bottom_frame, text="[ SYSTEM LOG ]", bg="#000", fg="#333", font=("Courier", 8)).pack(anchor="nw", padx=5)
        
        # Terminal Text Widget
        self.terminal = tk.Text(bottom_frame, bg="#000", fg="#00ff00", 
                               font=("Consolas", 9), height=8, state="disabled", bd=0)
        self.terminal.pack(fill="both", padx=10, pady=5)
        self.log("System initialized. Waiting for BCI headset...")

        # 3. ORTA ALAN (Paneller)
        content_frame = tk.Frame(self.root, bg=self.colors["bg"])
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # --- SOL PANEL: KONTROLLER ---
        left_panel = tk.Frame(content_frame, bg=self.colors["panel_bg"], width=200)
        left_panel.pack(side="left", fill="y", padx=5)
        
        tk.Label(left_panel, text="SİMÜLASYONLAR", bg=self.colors["panel_bg"], fg="white", font=("Arial", 10, "bold")).pack(pady=15)
        
        # Buton Stili
        btn_style = {"bg": "#222", "fg": "white", "bd": 1, "relief": "flat", "width": 20, "pady": 5, "cursor": "hand2"}
        
        tk.Button(left_panel, text="▶ CANLI AKIŞI BAŞLAT", **btn_style, command=self.toggle_stream).pack(pady=5, padx=10)
        tk.Frame(left_panel, height=2, bg="#333").pack(fill="x", pady=10, padx=10)
        
        tk.Label(left_panel, text="KOMUT TESTLERİ", bg=self.colors["panel_bg"], fg="#777", font=("Arial", 8)).pack(pady=5)
        
        self.btn_nav = tk.Button(left_panel, text="Navigasyon: Ev", **btn_style, command=lambda: self.run_command_scenario("Navigasyon: Eve rota oluştur.", "alpha"))
        self.btn_nav.pack(pady=2)
        
        self.btn_drone = tk.Button(left_panel, text="Drone: Kalkış", **btn_style, command=lambda: self.run_command_scenario("Drone Protokolü: Kalkış Onaylandı.", "beta"))
        self.btn_drone.pack(pady=2)
        
        self.btn_light = tk.Button(left_panel, text="IoT: Işıkları Aç", **btn_style, command=lambda: self.run_command_scenario("IoT Ağı: Salon Işıkları %100", "gamma"))
        self.btn_light.pack(pady=2)

        tk.Frame(left_panel, height=20, bg=self.colors["panel_bg"]).pack()
        
        # Slider (Gain Kontrolü)
        tk.Label(left_panel, text="Sinyal Hassasiyeti (Gain)", bg=self.colors["panel_bg"], fg="#ccc", font=("Arial", 8)).pack()
        self.slider = ttk.Scale(left_panel, from_=0.5, to=3.0, orient="horizontal", command=self.update_gain)
        self.slider.set(1.0)
        self.slider.pack(pady=5, padx=10, fill="x")

        # --- ORTA PANEL: MULTI-CHANNEL EEG ---
        center_panel = tk.LabelFrame(content_frame, text=" 4-Kanal Ham EEG Verisi ", 
                                    bg=self.colors["panel_bg"], fg=self.colors["text_dim"], font=("Courier", 10))
        center_panel.pack(side="left", expand=True, fill="both", padx=5)
        
        self.canvases = []
        for i, channel_name in enumerate(self.channels):
            # Her kanal için bir frame ve label
            ch_frame = tk.Frame(center_panel, bg=self.colors["panel_bg"], height=100)
            ch_frame.pack(fill="x", expand=True, padx=5, pady=2)
            ch_frame.pack_propagate(False) # Boyutu sabitle
            
            tk.Label(ch_frame, text=channel_name, bg=self.colors["panel_bg"], fg=self.colors["accent"], 
                     font=("Consolas", 8), anchor="w").pack(side="top", fill="x")
            
            cv = tk.Canvas(ch_frame, bg="#000", height=80, highlightthickness=0)
            cv.pack(fill="both", expand=True)
            self.canvases.append(cv)

        # --- SAĞ PANEL: ANALİZ (FFT & RESULTS) ---
        right_panel = tk.Frame(content_frame, bg=self.colors["bg"], width=250)
        right_panel.pack(side="right", fill="y", padx=5)
        
        # Spektrum Analizi
        fft_frame = tk.LabelFrame(right_panel, text=" Frekans Spektrumu ", 
                                 bg=self.colors["panel_bg"], fg=self.colors["text_dim"])
        fft_frame.pack(fill="x", pady=0, ipady=10)
        
        self.fft_canvas = tk.Canvas(fft_frame, bg="#000", height=150, highlightthickness=0)
        self.fft_canvas.pack(fill="x", padx=5, pady=5)
        
        # Sonuç Kutusu
        res_frame = tk.LabelFrame(right_panel, text=" Dekoder Çıktısı ", 
                                 bg=self.colors["panel_bg"], fg=self.colors["text_dim"])
        res_frame.pack(fill="both", expand=True, pady=10)
        
        self.lbl_process_status = tk.Label(res_frame, text="BEKLEMEDE", bg=self.colors["panel_bg"], fg="#555", font=("Arial", 10, "bold"))
        self.lbl_process_status.pack(pady=20)
        
        self.progress_bar = ttk.Progressbar(res_frame, length=200, mode='determinate')
        self.progress_bar.pack(padx=20, pady=5)
        
        self.lbl_final_command = tk.Label(res_frame, text="", bg=self.colors["panel_bg"], fg="white", 
                                         font=("Courier", 14, "bold"), wraplength=200)
        self.lbl_final_command.pack(pady=20)

    # --- SİSTEM MANTIKLARI ---
    
    def log(self, message):
        """Terminal çıktısı üretir."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        formatted_msg = f"[{timestamp}] > {message}\n"
        
        self.terminal.config(state="normal")
        self.terminal.insert("end", formatted_msg)
        self.terminal.see("end") # En alta kaydır
        self.terminal.config(state="disabled")

    def update_gain(self, val):
        self.gain = float(val)

    def toggle_stream(self):
        if not self.is_running:
            self.is_running = True
            self.lbl_connection.config(text="● CANLI BAĞLANTI AKTİF", fg=self.colors["success"])
            self.log("Connection established with NeuroSet-X1.")
            self.log("Signal quality: %98. Starting data stream...")
            self.animate_loop()
        else:
            self.is_running = False
            self.lbl_connection.config(text="● BAĞLANTI DURAKLATILDI", fg=self.colors["warning"])
            self.log("Stream paused by user.")

    def start_system_idle(self):
        """Uygulama açılınca boş grafikler çizmesin diye."""
        pass

    def animate_loop(self):
        if not self.is_running: return

        # 1. EEG ÇİZİMİ (4 KANAL)
        for i, canvas in enumerate(self.canvases):
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            canvas.delete("all")
            
            points = []
            cy = h / 2
            
            # Her kanal için hafif farklı frekanslar (Lob farkı simülasyonu)
            freq_offset = (i + 1) * 0.02 
            
            for x in range(0, w, 4):
                # Karmaşık dalga fonksiyonu
                y = cy + (math.sin((x + self.wave_phase) * (0.05 + freq_offset)) * 20 * self.gain) + \
                         (math.sin((x - self.wave_phase) * 0.1) * 10 * self.gain) + \
                         random.uniform(-3, 3)
                points.append(x)
                points.append(y)
            
            # Rengi kanala göre değiştir
            color = self.colors["accent"] if i % 2 == 0 else self.colors["secondary"]
            canvas.create_line(points, fill=color, width=2)
            
            # Izgara çizgisi (Estetik)
            canvas.create_line(0, cy, w, cy, fill="#222", width=1, dash=(2, 4))

        # 2. FFT SPEKTRUM ANALİZİ (Görsel Barla)
        self.fft_canvas.delete("all")
        fw = self.fft_canvas.winfo_width()
        fh = self.fft_canvas.winfo_height()
        bar_count = 20
        bar_w = fw / bar_count
        
        for b in range(bar_count):
            # Rastgele yükseklik ama yumuşak geçişli gibi (Perlin noise taklidi yok, random var)
            bar_h = random.randint(10, int(fh * 0.8)) * self.gain
            x1 = b * bar_w + 2
            y1 = fh - bar_h
            x2 = x1 + bar_w - 4
            y2 = fh
            
            # Frekansa göre renk (Düşükler yeşil, yüksekler kırmızı gibi)
            c_hex = "#00ffcc"
            if b > 15: c_hex = "#ff3333"
            elif b > 10: c_hex = "#1900ff"
            
            self.fft_canvas.create_rectangle(x1, y1, x2, y2, fill=c_hex, outline="")

        self.wave_phase += 5
        self.root.after(30, self.animate_loop)

    # --- SENARYO MOTORU ---
    def run_command_scenario(self, command_text, wave_type):
        if not self.is_running:
            self.log("ERROR: Cannot execute command. Stream is offline.")
            return

        self.log(f"Initiating sequence for pattern: {wave_type.upper()}")
        self.lbl_process_status.config(text="VERİ İŞLENİYOR...", fg=self.colors["warning"])
        self.progress_bar['value'] = 0
        
        # Adım 1: Progress Bar Doldur
        self.update_progress(0, command_text)

    def update_progress(self, val, cmd_text):
        if val <= 100:
            self.progress_bar['value'] = val
            self.root.after(30, self.update_progress, val + 2, cmd_text)
        else:
            # İşlem bitti
            self.log("Pattern match found (Confidence: 94%).")
            self.lbl_process_status.config(text="KOMUT ÇÖZÜMLENDİ", fg=self.colors["success"])
            self.lbl_final_command.config(text="")
            self.type_command(cmd_text, 0)

    def type_command(self, text, index):
        if index < len(text):
            current = self.lbl_final_command.cget("text")
            self.lbl_final_command.config(text=current + text[index])
            self.root.after(50, self.type_command, text, index + 1)
        else:
            self.log(f"Command executed: '{text}'")
            self.root.after(3000, self.reset_status)

    def reset_status(self):
        self.lbl_process_status.config(text="BEKLEMEDE", fg="#555")
        self.lbl_final_command.config(text="")
        self.progress_bar['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroSyncPro(root)
    root.mainloop()
    import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import datetime

class NeuroSyncFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroSync OS v3.2 [FINAL SHUTDOWN PROTOCOL]")
        self.root.geometry("1200x850")
        self.root.configure(bg="#050505")
        
        # X tuşuna basılınca özel kapanış senaryosu çalışsın
        self.root.protocol("WM_DELETE_WINDOW", self.system_shutdown_sequence)

        # --- Renk Paleti ---
        self.colors = {
            "bg": "#050505",
            "panel_bg": "#0f0f0f",
            "accent": "#00ffcc",    
            "secondary": "#ff00ff", 
            "grid": "#1a1a1a",
            "text_main": "#e0e0e0",
            "text_dim": "#555555",
            "success": "#00ff99",
            "warning": "#ffcc00",
            "danger": "#ff3333"
        }

        self.is_running = False
        self.wave_phase = 0
        self.channels = ["Fp1 (Frontal)", "P3 (Parietal)", "T7 (Temporal)", "O1 (Occipital)"]
        self.gain = 1.0
        
        # Arayüzü Kur
        self.create_menu()
        self.setup_layout()
        
        # Grafik motorunun ısınması için güncelleme (Donmayı önler)
        self.root.update_idletasks()
        
        # Açılış Logları
        self.safe_log("BIOS Integrity Check... OK")
        self.root.after(1000, lambda: self.safe_log("Loading Neural Drivers... OK"))
        self.root.after(1500, lambda: self.safe_log("System Ready. Waiting for user input."))

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sistem", menu=file_menu)
        file_menu.add_command(label="Güvenli Çıkış", command=self.system_shutdown_sequence)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Hakkında", command=self.show_about)

    def setup_layout(self):
        # HEADER
        header = tk.Frame(self.root, bg=self.colors["panel_bg"], height=60)
        header.pack(side="top", fill="x")
        tk.Label(header, text="NEUROSYNC // OS", bg=self.colors["panel_bg"], fg=self.colors["accent"], font=("Impact", 18)).pack(side="left", padx=20, pady=10)
        
        # TERMINAL
        bottom = tk.Frame(self.root, bg="#000", height=150)
        bottom.pack(side="bottom", fill="x")
        self.terminal = tk.Text(bottom, bg="#000", fg="#00ff00", font=("Consolas", 9), height=8, state="disabled", bd=0)
        self.terminal.pack(fill="both", padx=10, pady=5)

        # CONTENT
        content = tk.Frame(self.root, bg=self.colors["bg"])
        content.pack(expand=True, fill="both", padx=10, pady=10)

        # LEFT PANEL
        left = tk.Frame(content, bg=self.colors["panel_bg"], width=220)
        left.pack(side="left", fill="y", padx=5)
        
        tk.Label(left, text="KONTROL PANELİ", bg=self.colors["panel_bg"], fg="white", font=("Arial", 10, "bold")).pack(pady=15)
        
        self.btn_stream = tk.Button(left, text="▶ BAĞLANTIYI BAŞLAT", bg="#222", fg="white", bd=1, relief="flat", width=22, pady=6, cursor="hand2", command=self.toggle_stream)
        self.btn_stream.pack(pady=5, padx=10)
        
        tk.Label(left, text="----------------", bg=self.colors["panel_bg"], fg="#333").pack(pady=5)
        
        # Test Butonları (İkinci Kısımdaki Komutlar)
        btns = [("Drone Kaldır", "beta"), ("Işıkları Aç", "alpha"), ("Rotayı Çiz", "gamma")]
        for txt, wav in btns:
            tk.Button(left, text=f"[TEST] {txt}", bg="#222", fg="white", bd=1, relief="flat", width=22, pady=6, 
                      command=lambda t=txt, w=wav: self.run_scenario(t, w)).pack(pady=2)

        # Slider
        tk.Label(left, text="Sinyal Kazancı (Gain)", bg=self.colors["panel_bg"], fg="#777", font=("Arial", 8)).pack(pady=(20, 5))
        self.gain_slider = ttk.Scale(left, from_=0.1, to=5.0, command=self.update_gain)
        self.gain_slider.set(1.0)
        self.gain_slider.pack(fill="x", padx=20)

        # CENTER PANEL (Graphs)
        center = tk.LabelFrame(content, text=" CANLI EEG AKIŞI ", bg=self.colors["panel_bg"], fg="#888")
        center.pack(side="left", expand=True, fill="both", padx=5)
        
        self.canvases = []
        for ch in self.channels:
            f = tk.Frame(center, bg=self.colors["panel_bg"], height=80)
            f.pack(fill="x", expand=True, padx=5, pady=2)
            f.pack_propagate(False)
            tk.Label(f, text=ch, bg=self.colors["panel_bg"], fg=self.colors["accent"], font=("Consolas", 8)).pack(anchor="w")
            c = tk.Canvas(f, bg="black", height=60, highlightthickness=0)
            c.pack(fill="both", expand=True)
            self.canvases.append(c)

        # RIGHT PANEL (Analysis)
        right = tk.Frame(content, bg=self.colors["bg"], width=250)
        right.pack(side="right", fill="y", padx=5)
        
        self.fft_canvas = tk.Canvas(right, bg="black", height=200, highlightthickness=1, highlightbackground="#333")
        self.fft_canvas.pack(fill="x", pady=(20,0))
        
        self.lbl_status = tk.Label(right, text="BEKLEMEDE", bg="#111", fg="#555", font=("Arial", 12, "bold"), pady=10)
        self.lbl_status.pack(fill="x", pady=20)
        
        self.progress = ttk.Progressbar(right, length=100, mode='determinate')
        self.progress.pack(fill="x")
        
        self.lbl_result = tk.Label(right, text="", bg=self.colors["bg"], fg="white", font=("Courier", 12), wraplength=200)
        self.lbl_result.pack(pady=10)

    # --- MANTIK ve GÜVENLİK ---

    def safe_log(self, msg):
        try:
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            self.terminal.config(state="normal")
            self.terminal.insert("end", f"[{ts}] {msg}\n")
            self.terminal.see("end")
            self.terminal.config(state="disabled")
        except: pass

    def update_gain(self, v): 
        try: self.gain = float(v)
        except: self.gain = 1.0

    def toggle_stream(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.btn_stream.config(text="■ BAĞLANTIYI KES", fg=self.colors["danger"])
            self.safe_log("EEG Stream Started.")
            self.animate()
        else:
            self.btn_stream.config(text="▶ BAĞLANTIYI BAŞLAT", fg="white")
            self.safe_log("EEG Stream Paused.")

    def animate(self):
        if not self.is_running: return
        try:
            # Grafik Çizimleri (Optimize Edilmiş)
            for i, cv in enumerate(self.canvases):
                w = cv.winfo_width()
                h = cv.winfo_height()
                if w < 10: continue

                cv.delete("all")
                points = []
                cy = h / 2
                offset = (i + 1) * 0.2
                
                for x in range(0, w, 5):
                    val = math.sin((x + self.wave_phase) * (0.05 + offset)) * 20 * self.gain
                    noise = random.uniform(-2, 2)
                    y = cy + val + noise
                    points.extend([x, int(y)])
                
                if len(points) > 4:
                    color = self.colors["accent"] if i % 2 == 0 else self.colors["secondary"]
                    cv.create_line(points, fill=color, width=2)

            self.fft_canvas.delete("all")
            fw = self.fft_canvas.winfo_width()
            fh = self.fft_canvas.winfo_height()
            if fw > 10:
                bar_count = 15
                bar_w = fw / bar_count
                for i in range(bar_count):
                    bh = random.randint(5, int(fh * 0.8)) * self.gain
                    x1 = i * bar_w + 2
                    color = "#00ffcc" if i < 10 else "#ff3333"
                    self.fft_canvas.create_rectangle(x1, fh - bh, x1 + bar_w - 2, fh, fill=color, outline="")

            self.wave_phase += 5
        except Exception: pass
        self.root.after(40, self.animate)

    def run_scenario(self, cmd_text, wave_type):
        if not self.is_running:
            messagebox.showwarning("Hata", "Önce bağlantıyı başlatmalısın!")
            return
        self.safe_log(f"Processing: {wave_type}")
        self.lbl_status.config(text="ANALİZ EDİLİYOR...", fg=self.colors["warning"])
        self.lbl_result.config(text="")
        self.progress['value'] = 0
        self.process_step(0, cmd_text)

    def process_step(self, val, cmd):
        self.progress['value'] = val
        if val < 100:
            self.root.after(25, self.process_step, val + 2, cmd)
        else:
            self.progress['value'] = 100
            self.lbl_status.config(text="EŞLEŞME BULUNDU", fg=self.colors["success"])
            self.type_text(cmd, 0)

    def type_text(self, text, idx):
        if idx <= len(text):
            self.lbl_result.config(text=text[:idx])
            self.root.after(50, self.type_text, text, idx + 1)
        else:
            self.safe_log(f"EXEC: {text}")
            self.root.after(2000, lambda: self.lbl_status.config(text="BEKLEMEDE", fg="#555"))

    def show_about(self):
        messagebox.showinfo("Hakkında", "NeuroSync OS v3.2\nDeveloped by Fire Keskin")

    # --- FİNAL KAPANIŞ: TERSİNE İŞLEM PROTOKOLÜ ---
    def system_shutdown_sequence(self):
        """
        Sistemi kapatırken, daha önce yapılan işlemlerin tersini (Reversal) uygular.
        Açık olanı kapatır, kalkanı indirir.
        """
        self.is_running = False 
        
        # 1. Aşama: Arayüzü Kırmızı/Siyah Alarm Moduna Al
        self.root.configure(bg="#000000")
        for widget in self.root.winfo_children():
            widget.destroy() # Mevcut her şeyi sil
            
        # Kapanış Ekranı Başlığı
        lbl_title = tk.Label(self.root, text="SYSTEM SHUTDOWN INITIATED", 
                             bg="black", fg="red", font=("Courier", 30, "bold"))
        lbl_title.pack(pady=50)
        
        # Log Alanı (Tersine işlemleri listelemek için)
        self.shutdown_log = tk.Label(self.root, text="", bg="black", fg="#ff5555", font=("Consolas", 14), justify="left")
        self.shutdown_log.pack()
        
        # 2. Aşama: Tersine İşlemleri Sırayla Başlat (Zincirleme)
        self.root.after(500, lambda: self.append_shutdown_log("> Drone Uplink: LANDING SEQUENCE... [OK]"))
        self.root.after(1500, lambda: self.append_shutdown_log("> Smart Lights: POWERING OFF... [OK]"))
        self.root.after(2500, lambda: self.append_shutdown_log("> Navigation: ROUTE DELETED... [OK]"))
        self.root.after(3500, lambda: self.append_shutdown_log("> Neural Link: DISCONNECTING... [OK]"))
        
        # 3. Aşama: Programı Tamamen Kapat
        self.root.after(5000, self.root.destroy)

    def append_shutdown_log(self, text):
        current_text = self.shutdown_log.cget("text")
        self.shutdown_log.config(text=current_text + text + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroSyncFinal(root)
    root.mainloop()