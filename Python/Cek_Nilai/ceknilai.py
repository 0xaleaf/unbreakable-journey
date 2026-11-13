print("=== PROGRAM CEK KELULUSAN ===")

nama = input("Masukkan nama Mahasiswa: ")
nilai = int(input("Masukkan nilai Mahasiswa (1-100): "))

print("-" * 30)
print(f"Mahasiswa: {nama}")

if nilai >= 70:
    print("Status: SELAMAT, KAMU LULUS!.")
else:
    print("Status: MAAF, KAMU HARUS MENGULANG!.")