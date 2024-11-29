import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

def read_scenarios_from_file(filename):
    """Tek bir dosyadan birden fazla senaryoyu okur ve bir liste olarak döndürür."""
    with open(filename, 'r') as file:
        content = file.read()

    scenarios = []
    parts = content.strip().split('---')
    for part in parts:
        lines = part.strip().split('\n')
        if not lines or len(lines) < 3:
            continue

        # Senaryo adını al
        scenario_name = lines[0].strip('# ').strip()

        # Grid boyutu (satır ve sütun sayısı)
        grid_size = int(lines[1].strip())

        # Grid verileri
        grid = []
        for line in lines[2:]:
            if line.strip():
                row = [int(x) for x in line.strip().split()]
                grid.append(row)

        scenarios.append({
            'name': scenario_name,
            'grid_size': grid_size,
            'grid': grid
        })

    return scenarios

def find_nearest_parking_spot(grid, start):
    """En yakın boş park yerini BFS algoritması ile bulur ve en kısa yolu döndürür."""
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False]*cols for _ in range(rows)]
    parent = {}
    queue = []
    queue.append((start[0], start[1], 0))  # (x, y, mesafe)
    visited[start[0]][start[1]] = True

    while queue:
        x, y, dist = queue.pop(0)

        # Komşu hücreleri kontrol etme
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                if not visited[nx][ny]:
                    visited[nx][ny] = True
                    parent[(nx, ny)] = (x, y)
                    if grid[nx][ny] == 0:
                        # En uygun park yeri bulundu, yolu geri izleyelim
                        path = [(nx, ny)]
                        px, py = x, y
                        while (px, py) != start:
                            path.append((px, py))
                            px, py = parent[(px, py)]
                        path.append(start)
                        path.reverse()
                        return (nx, ny), dist + 1, path
                    else:
                        queue.append((nx, ny, dist + 1))

    return None, None, None  # Boş park yeri bulunamadı

def visualize_parking_grid(grid, start, nearest_spot, path, scenario_name):
    """Park alanını ve arabanın izlediği yolu görselleştirir."""
    grid_array = np.array(grid)
    plt.figure(figsize=(6, 6))
    plt.imshow(grid_array, cmap='Greys')

    # Boş park yerlerini yeşil ile işaretleme
    empty_spots = np.argwhere(grid_array == 0)
    for spot in empty_spots:
        plt.scatter(spot[1], spot[0], c='green', marker='s',s=400)

    # Dolu park yerlerini kırmızı ile işaretleme
    filled_spots = np.argwhere(grid_array == 1)
    for spot in filled_spots:
        plt.scatter(spot[1], spot[0], c='red', marker='s',s=400)

    # En uygun park yerini mavi ile işaretleme
    if nearest_spot:
        plt.scatter(nearest_spot[1], nearest_spot[0], c='blue', marker='s',s=400, label='En Uygun Park Yeri')

    # Başlangıç noktasını sarı ile işaretleme
    plt.scatter(start[1], start[0], c='yellow', marker='*', s=600, label='Başlangıç Noktası')

    # Yolu çizme
    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        plt.plot(path_x, path_y, c='orange', linewidth=2, label='İzlenen Yol')

    plt.title(f'Park Alanı Görselleştirme - {scenario_name}')
    plt.legend()

    # Eksenleri ayarlama ve indeksleri ekleme
    rows, cols = grid_array.shape
    plt.xticks(np.arange(cols), np.arange(cols))
    plt.yticks(np.arange(rows), np.arange(rows))
    plt.gca().invert_yaxis()
    plt.grid(True, color='black', linewidth=0.5)
    plt.show()

def run_gui(scenarios):
    current_scenario_index = 0

    def update_canvas():
        scenario = scenarios[current_scenario_index]
        scenario_name = scenario['name']
        grid = scenario['grid']

        # Sol çerçevede var olan canvas'ı temizleme
        for widget in left_frame.winfo_children():
            widget.destroy()

        # Park alanını sol tarafta görselleştireceğiz
        grid_array = np.array(grid)
        fig = plt.figure(figsize=(4, 4))
        plt.imshow(grid_array, cmap='Greys')

        # Boş park yerlerini yeşil ile işaretleme
        empty_spots = np.argwhere(grid_array == 0)
        for spot in empty_spots:
            plt.scatter(spot[1], spot[0], c='green', marker='s',s=400)

        # Dolu park yerlerini kırmızı ile işaretleme
        filled_spots = np.argwhere(grid_array == 1)
        for spot in filled_spots:
            plt.scatter(spot[1], spot[0], c='red', marker='s',s=400)

        # Eksenleri ayarlama ve indeksleri ekleme
        rows, cols = grid_array.shape
        plt.xticks(np.arange(cols), np.arange(cols))
        plt.yticks(np.arange(rows), np.arange(rows))
        plt.gca().invert_yaxis()
        plt.title(f'{scenario_name}')
        plt.axis('on')
        plt.grid(True, color='black', linewidth=0.5)

        # Canvas üzerine çizim yapma
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=left_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.close(fig)

    def set_start_point():
        try:
            x = int(entry_row.get())
            y = int(entry_col.get())
            scenario = scenarios[current_scenario_index]
            grid = [row[:] for row in scenario['grid']]
            rows = len(grid)
            cols = len(grid[0])

            if not (0 <= x < rows and 0 <= y < cols):
                messagebox.showerror("Hata", "Başlangıç noktası grid sınırları dışında.")
                return

            if grid[x][y] == 1:
                messagebox.showerror("Hata", "Başlangıç noktası dolu bir yer olamaz.")
                return

            grid[x][y] = 1  # Başlangıç noktasını dolu olarak işaretle

            nearest_spot, distance, path = find_nearest_parking_spot(grid, (x, y))

            if nearest_spot:
                messagebox.showinfo("Sonuç", f"En uygun park yeri: {nearest_spot}, Mesafe: {distance} birim")
                visualize_parking_grid(grid, (x, y), nearest_spot, path, scenario['name'])
            else:
                messagebox.showinfo("Sonuç", "Boş park yeri bulunamadı.")
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir sayı giriniz.")

    def next_scenario():
        nonlocal current_scenario_index
        if current_scenario_index < len(scenarios) - 1:
            current_scenario_index += 1
            update_canvas()
        else:
            messagebox.showinfo("Bilgi", "Son senaryodasınız.")

    def previous_scenario():
        nonlocal current_scenario_index
        if current_scenario_index > 0:
            current_scenario_index -= 1
            update_canvas()
        else:
            messagebox.showinfo("Bilgi", "İlk senaryodasınız.")

    # Ana pencere oluşturma
    root = tk.Tk()
    root.title("Park Yeri Bulma Uygulaması")

    # Sol ve sağ çerçeveleri oluşturma
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # Sol çerçevede park alanını güncelleme
    update_canvas()

    # Sağ çerçevede başlangıç noktası girişi
    label_row = tk.Label(right_frame, text="Başlangıç Noktası - Satır:")
    label_row.pack()
    entry_row = tk.Entry(right_frame)
    entry_row.pack()

    label_col = tk.Label(right_frame, text="Başlangıç Noktası - Sütun:")
    label_col.pack()
    entry_col = tk.Entry(right_frame)
    entry_col.pack()

    btn_set_start = tk.Button(right_frame, text="Başlangıç Noktasını Belirle", command=set_start_point)
    btn_set_start.pack(pady=10)

    # Senaryo değiştirme butonları
    btn_prev = tk.Button(right_frame, text="Önceki Senaryo", command=previous_scenario)
    btn_prev.pack(pady=5)
    btn_next = tk.Button(right_frame, text="Sonraki Senaryo", command=next_scenario)
    btn_next.pack(pady=5)

    root.mainloop()

def main():
    # Senaryoları okuma
    scenarios = read_scenarios_from_file('tests/scenarios.txt')

    # GUI uygulamasını çalıştırma
    run_gui(scenarios)

if __name__ == "__main__":
    main()
