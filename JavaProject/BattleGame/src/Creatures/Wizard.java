package creatures;

import interfaces.Healable;

public class Wizard extends Creature implements Healable {

    public Wizard(String name) {
        super(name, 80, 15);
    }

    @Override
    public void attack(Creature target) {
        System.out.println(name + " casts a magic missile!");
        target.receiveDamage(attackPower);
    }

    @Override
    public void specialMove(Creature target) {
        System.out.println(name + " casts Fireball!");
        target.receiveDamage(attackPower + 15);
    }

    @Override
    public void heal(int amount) {
        hp += amount;
        if (hp > 80) hp = 80;
        System.out.println(name + " heals for " + amount + " HP!");
    }
}
