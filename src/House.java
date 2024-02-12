import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

enum Situation{
    empty,rent,bought
}
public class House {
    final int ID;
    final int floor;
    final int meterage;
    final int numOfRooms;
    int numOfUser;


    List<Payment> debtReson = new ArrayList<>();
    List<Payment> paymentsHistory = new ArrayList<>();
    Situation situation;
    List<String> warnings = new ArrayList<>();

    public void changeSituation(Situation situation){
        this.situation = situation;
    }

    public House(int ID, int floor, int meterage, int numOfRooms, int numOfUser) {
        this.ID = ID;
        this.floor = floor;
        this.meterage = meterage;
        this.numOfRooms = numOfRooms;
        this.numOfUser = numOfUser;
    }
}

