# calen2025

日本の暦（旧暦、二十四節気、干支など）を計算するためのPythonライブラリ

## 必要条件

- Python 3.x
- ephemパッケージ

## インストール方法

```bash
pip install ephem
```

## 使用方法

```python
from calen2025.d3 import info

# 今日の暦情報を表示
print(info())

# 特定の日付の情報を取得
from calen2025.d3 import Day
d = Day(2025, 1, 1)  # 2025年1月1日の情報を取得
```

## 機能

- 二十四節気の計算
- 干支（十干十二支）の計算
- 九星の計算
- 旧暦の日付計算
- 六曜の計算
- 十二直の計算
- 二十八宿の計算
- 雑節の計算
- 暦注の計算
