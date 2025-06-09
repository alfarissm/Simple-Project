package creatures;

public class Warrior extends Creature {

    public Warrior(String name) {
        super(name, 100, 20);
    }

    @Override
    public void attack(Creature target) {
        System.out.println(name + " slashes with a sword!");
        target.receiveDamage(attackPower);
    }

    @Override
    public void specialMove(Creature target) {
        System.out.println(name + " performs Power Strike!");
        target.receiveDamage(attackPower + 10);
    }
}
