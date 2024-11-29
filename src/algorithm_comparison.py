import time
import tracemalloc
import heapq
from collections import deque
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
        if not lines or len(lines) < 4:
            continue

        # Senaryo adını al
        scenario_name = lines[0].strip('# ').strip()

        # Grid boyutu
        grid_size = int(lines[1].strip())

        # Başlangıç noktası
        start_coords = lines[2].strip().split()
        start_point = (int(start_coords[0]), int(start_coords[1]))

        # Grid verileri
        grid = []
        for line in lines[3:]:
            if line.strip():
                row = [int(x) for x in line.strip().split()]
                grid.append(row)

        scenarios.append({
            'name': scenario_name,
            'grid_size': grid_size,
            'start_point': start_point,
            'grid': grid
        })

    return scenarios

def bfs(grid, start):
    """BFS algoritması ile en yakın boş park yerini bulur."""
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    queue = deque()
    queue.append((start[0], start[1], 0))  # (x, y, mesafe)
    visited.add((start[0], start[1]))

    while queue:
        x, y, dist = queue.popleft()

        if grid[x][y] == 0 and (x, y) != start:
            return dist  # En kısa mesafe

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                if (nx, ny) not in visited and grid[nx][ny] != 1:
                    visited.add((nx, ny))
                    queue.append((nx, ny, dist + 1))

    return -1  # Boş park yeri bulunamadı

def dijkstra(grid, start):
    """Dijkstra algoritması ile en yakın boş park yerini bulur."""
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    heap = []
    heapq.heappush(heap, (0, start[0], start[1]))  # (mesafe, x, y)

    while heap:
        dist, x, y = heapq.heappop(heap)

        if (x, y) in visited:
            continue
        visited.add((x, y))

        if grid[x][y] == 0 and (x, y) != start:
            return dist  # En kısa mesafe

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                if (nx, ny) not in visited and grid[nx][ny] != 1:
                    heapq.heappush(heap, (dist + 1, nx, ny))

    return -1  # Boş park yeri bulunamadı

def a_star(grid, start):
    """A* algoritması ile en yakın boş park yerini bulur."""
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    heap = []
    heapq.heappush(heap, (heuristic(start, start), 0, start[0], start[1]))  # (f_score, g_score, x, y)

    while heap:
        f_score, g_score, x, y = heapq.heappop(heap)

        if (x, y) in visited:
            continue
        visited.add((x, y))

        if grid[x][y] == 0 and (x, y) != start:
            return g_score  # En kısa mesafe

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                if (nx, ny) not in visited and grid[nx][ny] != 1:
                    h = heuristic((nx, ny), start)
                    heapq.heappush(heap, (g_score + 1 + h, g_score + 1, nx, ny))

    return -1  # Boş park yeri bulunamadı

def heuristic(a, b):
    """Manhattan mesafesi hesaplar."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def measure_algorithm(algorithm, grid, start, runs=50):
    """Algoritmanın ortalama çalışma süresini ve bellek kullanımını ölçer."""
    total_time = 0
    total_memory = 0
    distances = []
    for _ in range(runs):
        tracemalloc.start()
        start_time = time.perf_counter()

        distance = algorithm(grid, start)

        current, peak = tracemalloc.get_traced_memory()
        end_time = time.perf_counter()
        tracemalloc.stop()

        time_elapsed = end_time - start_time
        memory_used = peak / 10**6  # Byte'dan MB'a çevir

        total_time += time_elapsed
        total_memory += memory_used
        distances.append(distance)

    average_time = total_time / runs
    average_memory = total_memory / runs
    # Mesafelerin tutarlı olması gerekir, ancak farklıysa en sık görüleni alıyoruz
    distance = max(set(distances), key=distances.count)
    return distance, average_time, average_memory


def run_tests(scenarios):
    """Tüm senaryolar ve algoritmalar için testleri çalıştırır."""
    results = []

    for scenario in scenarios:
        scenario_name = scenario['name']
        start_point = scenario['start_point']
        park_grid = scenario['grid']

        # Başlangıç noktasını dolu olarak ayarlama
        grid = [row[:] for row in park_grid]
        grid[start_point[0]][start_point[1]] = 1

        algorithms = [
            ('BFS', bfs),
            ('Dijkstra', dijkstra),
            ('A*', a_star)
        ]

        for algo_name, algo_func in algorithms:
            distance, time_elapsed, memory_used = measure_algorithm(algo_func, grid, start_point)

            results.append({
                'Senaryo': scenario_name,
                'Algoritma': algo_name,
                'Mesafe': distance,
                'Süre (s)': time_elapsed,
                'Bellek (MB)': memory_used
            })

    return results

def display_results(results):
    """Sonuçları konsola tablo şeklinde yazdırır."""
    print("\nSonuçlar:")
    print("{:<25} {:<10} {:<10} {:<15} {:<15}".format('Senaryo', 'Algoritma', 'Mesafe', 'Süre (s)', 'Bellek (MB)'))
    print("-" * 80)
    for res in results:
        print("{:<25} {:<10} {:<10} {:<15.6f} {:<15.3f}".format(
            res['Senaryo'], res['Algoritma'], res['Mesafe'], res['Süre (s)'], res['Bellek (MB)']
        ))

def plot_combined_results(results):
    """Süre ve bellek kullanımını tek bir grafik üzerinde yan yana gösterir."""
    scenarios = list(set([res['Senaryo'] for res in results]))
    scenarios.sort()
    algorithms = ['BFS', 'Dijkstra', 'A*']

    # Verileri hazırlama
    time_data = {algo: [] for algo in algorithms}
    memory_data = {algo: [] for algo in algorithms}

    for scenario in scenarios:
        for algo in algorithms:
            for res in results:
                if res['Senaryo'] == scenario and res['Algoritma'] == algo:
                    time_data[algo].append(res['Süre (s)'])
                    memory_data[algo].append(res['Bellek (MB)'])

    x = np.arange(len(scenarios))  # Senaryo sayısı kadar indeks
    total_width = 0.8
    bar_width = total_width / (len(algorithms) * 2)  # Süre ve bellek için

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Süre çubukları
    for i, algo in enumerate(algorithms):
        ax1.bar(x + (i - 1) * bar_width * 2, time_data[algo], width=bar_width, label=f"{algo} - Süre (s)")

    ax1.set_xlabel('Senaryolar')
    ax1.set_ylabel('Çalışma Süresi (s)')
    ax1.set_title('Algoritmaların Süre ve Bellek Kullanımı Karşılaştırması')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios, rotation=45)

    # Bellek kullanımını ikinci bir y ekseni olarak ekleyelim
    ax2 = ax1.twinx()
    # Bellek çubukları
    for i, algo in enumerate(algorithms):
        ax2.bar(x + (i - 1) * bar_width * 2 + bar_width, memory_data[algo], width=bar_width, label=f"{algo} - Bellek (MB)", alpha=0.7)

    ax2.set_ylabel('Bellek Kullanımı (MB)')

    # Her iki eksen için ortak bir lejant oluşturalım
    lines_labels = [ax.get_legend_handles_labels() for ax in [ax1, ax2]]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    plt.legend(lines, labels, loc='upper right')

    plt.tight_layout()
    plt.show()

def determine_best_algorithms(results):
    """Her senaryo için en iyi algoritmayı belirler ve sonucu yazdırır."""
    scenarios = list(set([res['Senaryo'] for res in results]))
    scenarios.sort()

    best_algorithms = []

    for scenario in scenarios:
        # Bu senaryoya ait sonuçları filtrele
        scenario_results = [res for res in results if res['Senaryo'] == scenario]

        # Algoritmaları süreye göre sıralama (birincil), bellek kullanımına göre sıralama (ikincil)
        sorted_algorithms = sorted(scenario_results, key=lambda x: (x['Süre (s)'], x['Bellek (MB)']))

        best_algorithm = sorted_algorithms[0]['Algoritma']
        best_time = sorted_algorithms[0]['Süre (s)']
        best_memory = sorted_algorithms[0]['Bellek (MB)']

        best_algorithms.append({
            'Senaryo': scenario,
            'En İyi Algoritma': best_algorithm,
            'Süre (s)': best_time,
            'Bellek (MB)': best_memory
        })

    # En iyi algoritmaları yazdırma
    print("\nEn İyi Algoritmalar:")
    print("{:<25} {:<15} {:<15} {:<15}".format('Senaryo', 'En İyi Algoritma', 'Süre (s)', 'Bellek (MB)'))
    print("-" * 70)
    for res in best_algorithms:
        print("{:<25} {:<15} {:<15.6f} {:<15.3f}".format(
            res['Senaryo'], res['En İyi Algoritma'], res['Süre (s)'], res['Bellek (MB)']
        ))

    return best_algorithms

def plot_best_algorithms(best_algorithms):
    """Her senaryo için en iyi algoritmayı grafik üzerinde gösterir."""
    scenarios = [res['Senaryo'] for res in best_algorithms]
    algorithms = [res['En İyi Algoritma'] for res in best_algorithms]

    # Algoritma isimlerini sayısal değerlere dönüştürme
    algo_mapping = {'BFS': 0, 'Dijkstra': 1, 'A*': 2}
    algo_numbers = [algo_mapping[algo] for algo in algorithms]

    plt.figure(figsize=(12, 6))
    plt.bar(scenarios, algo_numbers, color='skyblue')
    plt.xlabel('Senaryolar')
    plt.ylabel('En İyi Algoritma')
    plt.title('Her Senaryo İçin En İyi Algoritma')
    plt.xticks(rotation=45)

    # Y eksenindeki sayıları algoritma isimleriyle değiştirme
    plt.yticks(list(algo_mapping.values()), list(algo_mapping.keys()))

    plt.tight_layout()
    plt.show()

def main():
    # Senaryoları okuma
    scenarios = read_scenarios_from_file('tests/test_scenarios_for_comparison.txt')

    # Testleri çalıştırma
    results = run_tests(scenarios)

    # Sonuçları gösterme
    display_results(results)

    # Sonuçları grafiklerle gösterme
    plot_combined_results(results)

    # En iyi algoritmaları belirleme ve yazdırma
    best_algorithms = determine_best_algorithms(results)

    # En iyi algoritmaları grafikle gösterme
    plot_best_algorithms(best_algorithms)

if __name__ == "__main__":
    main()
