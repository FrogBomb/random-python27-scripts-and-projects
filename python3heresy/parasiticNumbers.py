import math
def findParasiticNumbers(multiplier, base = 10):
    if multiplier == 1:
        return [i for i in range(1, base)]
    if (multiplier >= base):
        raise f"Multipler {multiplier} must be less than the base {base}"
    
    unreduced_denominator = base * multiplier - 1
    
    gcds = {i: math.gcd(i, unreduced_denominator) for i in range(multiplier, base)}
    unitForGcd = {}
    for gcd in set(gcds.values()):
        denominator = unreduced_denominator // gcd
        divmods_of_base_powers = [divmod(base, denominator)]
        # Find the cycle...
        while((current_power_mod := divmods_of_base_powers[-1][-1]) != divmods_of_base_powers[0][-1] or len(divmods_of_base_powers) == 1):
            divmods_of_base_powers.append(divmod(current_power_mod * base, denominator))
        divmods_of_base_powers.pop()
        calcUnit = sum(d*base**i for (i, (d, _)) in enumerate(reversed(divmods_of_base_powers)))
        unitForGcd[gcd] = calcUnit

    return [unitForGcd[gcds[n]]*(n//gcds[n]) for n in range(multiplier, base)]

if __name__ == "__main__":
    import numpy as np
    print("Parasitic numbers (base numbers - all others can be found by self concatenation of each of these)\n\n")
    for base in range(2, 37
                      ):
        print(f"base-{base} parsitic numbers:")
        for i in range(1, base):
            numbers = findParasiticNumbers(i, base)
            min_number = np.base_repr(min(numbers), base)

            print("\t", end="")
            print(f"parsitic-{i} base-{base} numbers (min: {min_number}, length of min: {len(min_number)}):")
            print("\t\t", end="")
            print(*(np.base_repr(number, base) for number in numbers))
    