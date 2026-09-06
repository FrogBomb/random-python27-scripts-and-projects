def findParasiticNumbers(multiplier, base = 10):
    if multiplier == 1:
        return [i for i in range(1, base)]
    if (multiplier >= base):
        raise f"Multipler {multiplier} must be less than the base {base}"
    
    denominator = base * multiplier - 1
    divmods_of_base_powers = [divmod(base * base, denominator)]
    # Find the cycle...
    while((current_power_mod := divmods_of_base_powers[-1][-1]) != base):
        divmods_of_base_powers.append(divmod(current_power_mod * base, denominator))

    divmods_of_base_powers.insert(0, divmods_of_base_powers.pop())
    calcUnit = sum(d*base**i for (i, (d, _)) in enumerate(reversed(divmods_of_base_powers)))
    return [calcUnit * n for n in range(multiplier, base)]


for i in range(1, 10):
    print(f"parsitic-{i} of min length: {findParasiticNumbers(i)}")
    