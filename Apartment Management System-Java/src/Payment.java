import java.util.Comparator;

public class Payment {
     final int price;
     final PaymentReson paymentReson;
     final Date date;
     Date payDate = null;


    public Payment(int price, PaymentReson paymentReson, Date date) {
        this.price = price;
        this.paymentReson = paymentReson;
        this.date = date;
    }
}


enum PaymentReson{
    elecBill,waterBill,gasBill,rent,apartmentCharge,mortgage
}

class Date{
    int day,month,year;

    public Date(int day, int month, int year) {
        this.day = day;
        this.month = month;
        this.year = year;
        if(day > 31)this.day = 31;
        if(month > 12)this.month = 12;
    }

    public int compare(Date date){
        if(year > date.year){
            return 1;
        }else if(year == date.year){
            if(month>date.month){
                return 1;
            }else if (month == date.month){
                if(day > date.day){
                    return 1;
                }else if(day == date.day){
                    return 0;
                }else {
                    return -1;
                }
            }else {
                return -1;
            }
        }else{
            return -1;
        }
    }
}