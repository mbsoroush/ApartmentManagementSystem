package DataBase;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class SQLiteHelper implements IQuery{
	public String dbName;
	//Constructor
	public SQLiteHelper (String dbName) {
		this.dbName = dbName;
	}
	@Override
	public Connection getConnection() {
		
		try {
		DriverManager.registerDriver(new org.sqlite.JDBC());
		Connection conn = DriverManager.getConnection("jdbc:sqlite:" + dbName + ".db");
		return conn;
		}catch(SQLException e) {
			e.printStackTrace();
		}
		return null;
	}
	 public boolean configStructure() {
		 boolean status = false;
		 String createTableQuery = "CREATE TABLE IF NOT EXISTS resident(key INTEGER PRIMARY KEY ,first_name TEXT, last_name TEXT, id INTEGER );";
		 Connection conn = getConnection();
		 
		 try (Statement stmt = conn.createStatement() ){
			 stmt.execute(createTableQuery);
			 status = true;
			 
		 }catch (SQLException e) {
			 System.out.println(e.getMessage());
		 }
		 return status;
	 }
}
