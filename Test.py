r = 10

for row_number in range((2 * r) - 1):
    if row_number >= r:
        num_in_row = (2 * row_number) - (4 * (row_number - r + 1) - 1)
    else:
        num_in_row = (2 * row_number) + 1

    print "*" * num_in_row


