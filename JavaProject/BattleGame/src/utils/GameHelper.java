package utils;

import java.util.Scanner;

public class GameHelper {
    public static int getIntInput(Scanner scanner, String message) {
        System.out.print(message);
        while (!scanner.hasNextInt()) {
            scanner.next(); // clear invalid input
            System.out.print("Invalid input. " + message);
        }
        return scanner.nextInt();
    }
}
