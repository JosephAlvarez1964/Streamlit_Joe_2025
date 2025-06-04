def calcular_anualidad(F, i, n):
    """Calcula la anualidad necesaria para un fondo de amortización de anualidades vencidas."""
    A = F * i / ((1 + i) ** n - 1)
    return A

def tabla_fondo_amortizacion(F, i, n):
    A = calcular_anualidad(F, i, n)
    saldo = 0
    print(f"{'Año':<5}{'Depósito':<15}{'Interés':<15}{'Saldo Final':<15}")
    print("-" * 50)

    for año in range(1, n + 1):
        interes = saldo * i
        saldo += interes + A
        print(f"{año:<5}{A:<15.2f}{interes:<15.2f}{saldo:<15.2f}")

    print("\nMonto acumulado final: {:.2f}".format(saldo))
    print("Anualidad requerida: {:.2f}".format(A))

# Ejemplo de uso
F = 100000   # Monto futuro deseado
i = 0.08     # Tasa de interés anual (8%)
n = 10       # Número de años
