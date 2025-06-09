package creatures;

public class Archer extends Creature {

    public Archer(String name) {
        super(name, 90, 18);
    }

    @Override
    public void attack(Creature target) {
        System.out.println(name + " shoots an arrow!");
        target.receiveDamage(attackPower);
    }

    @Override
    public void specialMove(Creature target) {
        System.out.println(name + " performs Rapid Shot!");
        target.receiveDamage(attackPower / 2);
        target.receiveDamage(attackPower / 2);
        target.receiveDamage(attackPower);
    }
}
