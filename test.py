
import pprint

inline_keyboard = []
row = []
inline_number = 1

for i in range(1, 15):
    row.append(inline_number)
    if i % 3 == 0:
        inline_keyboard.append(row)
        row = []
    inline_number += 1

# Add the remaining numbers if any
if row:
    inline_keyboard.append(row)

pprint.pprint(inline_keyboard)