package DataBase;

public class Resident {
	private int key;
	private String firstName;
	private String lastName;
	private int id;
	
	public Resident(int key, String firstName, String lastName, int id) {
	    this.key = key;
		this.firstName = firstName;
		this.lastName = lastName;
		this.id = id;
	}
	public Resident() {
		this(0, "", "", 0);
	}
	public Resident(int key) {
		this(key, "", "", 0);
	}
	public void setKey(int key) {
		this.key = key;
	}
	public int getKey() {
		return key;
	}
	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}
	public String getFirstName() {
		return firstName;
	}
	public void setLastName(String lastname) {
		this.lastName = lastname;
	}
	public String getlastName() {
		return lastName;
	}
	public void setId(int id) {
		this.id = id;
	}
	public int getId() {
		return id;
	}
	@Override
	public String toString() {
		return "resident model (" + key + ") : { first_name = " + firstName + ", last_name = " + lastName + ", id = " + id + " }";
	}

}
*/
