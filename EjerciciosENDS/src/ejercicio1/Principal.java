package ejercicio1;

import java.util.Scanner;

public class Principal {
	public static void main(String[] args) {
			Scanner sc = new Scanner(System.in);
			System.out.println("\nBienvenid@, este programa mostrará la tirada de 3 dados y realizará la suma total.");
			System.out.println("-----------------------------------------------------------------------------");
			System.out.println();
			int contador = 1;
			int suma = 0;
			//hay que cambiar y poner < 4 para que no entre una 4ª vez
			for (int i = 1; i < 4; i++) {
				//Math.random genera nums entre el 0 y 0.9999. Si pones * 6, generará entre 0 y 5.999. 
				// Al poner +1, decimos que se desplace uno, es decir, empiece en 1 y acabe el 6.999. Al ser int, entre 1 y 6
				int dado = (int)(Math.random()*6+1); 
				System.out.println("El dado " + contador + " ha sacado: "
					+ dado);
				suma = suma + dado;
				contador++;
				System.out.println();
		}
		System.out.println("\nLa suma total de los 3 dados es " + suma);
	}
}
