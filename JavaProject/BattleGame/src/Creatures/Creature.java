package creatures;

import interfaces.Attackable;

public abstract class Creature implements Attackable {
    protected String name;
    protected int hp;
    protected int attackPower;

    public Creature(String name, int hp, int attackPower) {
        this.name = name;
        this.hp = hp;
        this.attackPower = attackPower;
    }

    public boolean isAlive() {
        return hp > 0;
    }

    public void receiveDamage(int damage) {
        hp -= damage;
        if (hp < 0) hp = 0;
        System.out.println(name + " received " + damage + " damage!");
    }

    public void displayStatus() {
        System.out.println(name + " HP: " + hp);
    }

    public abstract void specialMove(Creature target);
}
