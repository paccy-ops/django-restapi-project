data = {
    "Feltnr 0013": "79.897,00",
    "Feltnr 0015": "20.220,00",
    "Feltnr 0016": "1.250,00",
    "Feltnr 0020": "1.704,06",
    "Feltnr 0046": "1.995,20",
    "Feltnr 0048": "7.396,99",
    "Feltnr 0147": "16.667,50",
    "Feltnr 0148": "432,28",
    "Feltnr 0200": "2,08",
    "Feltnr 0202": "953,32",
    "period": "Feb 1 - 28"
}


def calculate_total_amount(datas):
    total = 0
    for d in datas:
        if d == "period":
            continue
        se = data[d].replace(',', '')
        dr = float(se)
        total += dr
    return total
