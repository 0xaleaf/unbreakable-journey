package Java;

import java.util.Scanner;

public class ceknilai {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.println("=== PROGRAM CEK KULULUSAN (JAVA)");

        System.out.print("Masukkan nama Mahasiswa: ");
        String nama = input.nextLine();

        System.out.print("Masukkan nilai Mahasiswa (0-100): ");
        int nilai = input.nextInt();

        System.out.println("------------------------------");
        System.out.println("Mahasiswa: " + nama);

        if (nilai >= 75) {
            System.out.println("Status: SELAMAT, KAMU LULUS!");
        } else {
            System.out.println("Status: MAAF, KAMU HARUS MENGULANG.");
        }
        input.close();
    }
}
