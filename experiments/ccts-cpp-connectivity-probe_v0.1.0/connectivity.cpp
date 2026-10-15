// CCTS experimental kernel / CCTS 實驗用運算核心。
// This function checks undirected graph connectivity after Python validates
// source roles, edge relations, and provenance. It is NOT a CCTS admission gate.
// 本函式僅在 Python 已驗證角色、修訂關係及來源歸屬後檢查無向圖連通性；
// 並非 CCTS 准入判定器，也不得取代現有 Python 驗證。

#include <cstdint>
#include <numeric>
#include <vector>

// n：節點數；m：邊數；pairs：依序排列的 (來源節點, 目標節點) 整數索引。
// 回傳：1=連通、0=不連通、-1=輸入不合法或運算失敗。
// 不接受空圖、自連線、超出範圍的節點或不合理大的輸入。
extern "C" int ccts_graph_connected(std::uint32_t n, std::uint32_t m,
                                      const std::uint32_t* pairs) noexcept {
    if (n == 0 || n > 10000 || m > 100000 || (m != 0 && pairs == nullptr)) {
        return -1;
    }

    try {
        // 使用並查集（Disjoint Set Union）將每條邊兩端的節點合併。
        // 每個連通分量最終有一個根節點；只有一個根即為連通。
        std::vector<std::uint32_t> parent(n);
        std::iota(parent.begin(), parent.end(), 0U);
        auto find_root = [&parent](std::uint32_t node) {
            while (parent[node] != node) {
                parent[node] = parent[parent[node]];
                node = parent[node];
            }
            return node;
        };

        for (std::uint32_t index = 0; index < m; ++index) {
            const auto left = pairs[2U * index];
            const auto right = pairs[2U * index + 1U];
            if (left >= n || right >= n || left == right) {
                return -1;
            }
            parent[find_root(left)] = find_root(right);
        }

        const auto root = find_root(0);
        for (std::uint32_t node = 1; node < n; ++node) {
            if (find_root(node) != root) {
                return 0;
            }
        }
        return 1;
    } catch (...) {
        // C++ 例外不越過 C 語言 ABI；以明確錯誤碼回報。
        return -1;
    }
}
