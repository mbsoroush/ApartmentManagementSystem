import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Customer extends Person{
    //boolean rentOrOwn;//true for own and false for rent
    House house;

    public void changeSitRequest(Situation situation) throws InvalidRequestException{
        if(house.situation.equals(Situation.rent)){
            if(situation.equals(Situation.rent)){
                throw new InvalidRequestException("you cant rent a house that has been rent");
            }
        }else if(house.situation.equals(Situation.bought)){
            if(situation.equals(Situation.rent)){
                throw new InvalidRequestException("you cant rent your house");
            }
        }
        //request to manager needs
    }

    public Customer(String name,String lastName,House house,String password) {
        super.password = password;
        //this.rentOrOwn = rentOrOwn;
        super.name = name;
        super.lastName = lastName;
        this.house = house;
    }

    public List<Payment> timedPayments(){
        return house.paymentsHistory.stream().sorted((a1,a2) -> (a1.date.compare(a2.date))).toList();
    }

    public List<Payment> filteredPaymentList(PaymentReson paymentReson){
        return house.paymentsHistory.stream().filter(p -> p.paymentReson.equals(paymentReson)).toList();
    }

    public List<Payment> timeFilterPaymentList(Date date1,Date date2){
        return house.paymentsHistory.stream().filter(p -> (p.date.compare(date1) > 0)&&(p.date.compare(date2) < 0)).
                sorted((a1,a2) -> (a1.date.compare(a2.date))).toList();
    }

    public Map<Integer,PaymentReson> debts(){
        Map<Integer,PaymentReson> debtReson = new HashMap<>();
        for(Payment p: house.debtReson){
            debtReson.put(p.price,p.paymentReson);
        }
        return debtReson;
    }
}
