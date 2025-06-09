import java.util.Random;
import java.util.Scanner;

import creatures.Archer;
import creatures.Creature;
import creatures.Warrior;
import creatures.Wizard;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random rand = new Random();
        System.out.println("Battle Game by Alfaris (2023071028)");
        System.out.println("Welcome to Battle of Creatures!");
        System.out.println("Choose your character:");
        System.out.println("1. Warrior");
        System.out.println("2. Wizard");
        System.out.println("3. Archer");

        int choice = scanner.nextInt();
        Creature player;

        switch (choice) {
            case 1:
                player = new Warrior("Player Warrior");
                break;
            case 2:
                player = new Wizard("Player Wizard");
                break;
            case 3:
                player = new Archer("Player Archer");
                break;
            default:
                System.out.println("Invalid choice.");
                return;
        }

        // Random enemy: Warrior, Wizard, or Archer
        Creature enemy;
        int enemyType = rand.nextInt(3); // 0, 1, or 2
        switch (enemyType) {
            case 0:
                enemy = new Warrior("Enemy Warrior");
                break;
            case 1:
                enemy = new Wizard("Enemy Wizard");
                break;
            case 2:
                enemy = new Archer("Enemy Archer");
                break;
            default:
                enemy = new Warrior("Enemy Backup");
        }

        System.out.println("\nBattle Start!");
        player.displayStatus();
        enemy.displayStatus();
        System.out.println();

        while (player.isAlive() && enemy.isAlive()) {
            // Player turn
            System.out.println("\nYour Turn:");
            System.out.println("1. Normal Attack");
            System.out.println("2. Special Move");
            if (player instanceof interfaces.Healable) {
                System.out.println("3. Heal");
            }

            int action = scanner.nextInt();

            switch (action) {
                case 1:
                    player.attack(enemy);
                    break;
                case 2:
                    player.specialMove(enemy);
                    break;
                case 3:
                    if (player instanceof interfaces.Healable) {
                        ((interfaces.Healable) player).heal(20);
                    } else {
                        System.out.println("You can't heal!");
                    }
                    break;
                default:
                    System.out.println("Invalid action. Skipped turn.");
            }

            if (!enemy.isAlive()) break;

            // Enemy turn
            System.out.println("\nEnemy's Turn:");
            if (rand.nextBoolean()) {
                enemy.attack(player);
            } else {
                enemy.specialMove(player);
            }

            // Display status
            System.out.println("\nStatus:");
            player.displayStatus();
            enemy.displayStatus();
        }

        // Game over
        System.out.println("\nBattle Over!");
        if (player.isAlive()) {
            System.out.println("You Win!");
        } else {
            System.out.println("You Lose!");
        }
    }
}
