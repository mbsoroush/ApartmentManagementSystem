/*package DataBase;

import DataBase.SQLiteHelper;
import DataBase.SQLiteHandler;
import DataBase.Resident;
public class Test {

	public static void main(String[] args) {
	
		//SQLiteHelper helper = new SQLiteHelper("test");
		SQLiteHandler handler  = new SQLiteHandler("test");
		/*if(helper.getConnection() != null) {
			System.out.println("OK");
		}else {
			System.out.println("Problem");
		}*/
		//CreatTable
		//System.out.println(helper.configStructure());
		//Insert
		//handler.insert(new Resident(1214, "navid", "mahjoob", 3));
		//handler.insert(new Resident(1315, "ashkan", "sohrabi", 4));
		/*Resident resident = new Resident(6589, "alireza", "naghavi", 2);
		System.out.println(handler.insert(resident));*/
		//SelectAll
		//System.out.println(handler.selectAllResidents());
		//Select
		/*Resident resident = new Resident();
		resident.setFirstName("ashkan");
		resident.setLastName("sohrabi");
		resident = handler.select(resident);
		System.out.println(resident);*/
		//NewSelect
		//System.out.println(handler.select(new Resident(1315)));
		//SelectLimited
		//System.out.println(handler.selectLimitedResidents(2, 0));
		//CheckSimilarKey
		//System.out.println(handler.insert(new Resident(1214, "alireza", "naghavi", 7)));
		//System.out.println(handler.selectAllResidents());
		//Remove
		/*System.out.println(handler.remove(new Resident(1256)));
		System.out.println(handler.selectAllResidents());*/
		//Update
		/*System.out.println(handler.selectAllResidents());
		Resident model = handler.select(new Resident(1214));
		model.setFirstName("mohammad navid");
		model.setId(1);
		System.out.println(handler.update(model)); //true or false
		System.out.println(handler.selectAllResidents());
	}
}*/
