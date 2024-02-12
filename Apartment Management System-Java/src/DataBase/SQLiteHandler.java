package DataBase;
/*import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.*;

public class SQLiteHandler {
	SQLiteHelper helper;
	//constructor
	public SQLiteHandler (String dbName) {
		helper = new SQLiteHelper(dbName);
		}
	public boolean insert (Resident model) {
		boolean status = false;
		
		Resident tmp = select(new Resident(model.getKey()));
		if(!tmp.getFirstName().equals("")) return status;
		
		String query = "INSERT INTO resident(key, first_name, last_name, id) VALUES(?,?,?,?)";
		
		try (Connection conn = helper.getConnection();
			 PreparedStatement pstmt = conn.prepareStatement(query)) {
			
			pstmt.setInt(1, model.getKey());
			pstmt.setString(2, model.getFirstName());
			pstmt.setString(3, model.getlastName());
			pstmt.setInt(4, model.getId());
		    pstmt.executeUpdate();
		    status = true;
		    
		}catch (SQLException e) {
			System.out.println(e.getMessage());
		}
		return status;
	}
	//SelectAll
	public List<Resident> selectAllResidents(){
		List<Resident> models = new LinkedList<Resident>();
		String query = "SELECT key, first_name, last_name, id FROM resident";
		
		try(Connection conn = helper.getConnection();
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery(query)){
			while(rs.next()) {
				Resident model = new Resident();
				model.setKey(rs.getInt("key"));
				model.setFirstName(rs.getString("first_name"));
				model.setLastName(rs.getString("last_name"));
				model.setId(rs.getInt("id"));
				models.add(model);
			}
		}catch(SQLException e) {
			System.out.println(e.getMessage());
		}
		
		return models;
	}
	//Select
	public Resident select(Resident model) {
		String query = "SELECT first_name, last_name, id FROM resident WHERE key = ?";
		
		try(Connection conn = helper.getConnection();
			PreparedStatement pstmt = conn.prepareStatement(query);){
			
			pstmt.setInt(1, model.getKey());
			ResultSet rs = pstmt.executeQuery();
			
			while(rs.next()) {
				model.setFirstName(rs.getString("first_name"));
				model.setLastName(rs.getString("last_name"));
				model.setId(rs.getInt("id"));
			}
			rs.close();
	}catch(SQLException e) {
		System.out.println(e.getMessage());
	}
	return model;
	}
	//SelectLimited
	public List<Resident> selectLimitedResidents(int limit, int offset){
		List<Resident> models = new LinkedList<Resident>();
		String query = "SELECT key, first_name, last_name, id FROM resident LIMIT ? OFFSET ?";
		
		try (Connection conn = helper.getConnection();
			 PreparedStatement pstmt = conn.prepareStatement(query);){
			
			 pstmt.setInt(1, limit);
			 pstmt.setInt(2, offset);
			 ResultSet rs = pstmt.executeQuery();
			 
			 while(rs.next()) {
				 Resident model = new Resident();
				 model.setKey(rs.getInt("key"));
				 model.setFirstName(rs.getString("first_name"));
				 model.setLastName(rs.getString("last_name"));
				 model.setId(rs.getInt("id"));
				 models.add(model);
			 }
			 rs.close();
		}catch(SQLException e) {
			System.out.println(e.getMessage());
		}
		return models;
	}
	//Remove
	public boolean remove(Resident model) {
		boolean status = false;
		String query = "DELETE FROM resident WHERE key = ?";
		
		try (Connection conn = helper.getConnection();
			 PreparedStatement pstmt = conn.prepareStatement(query)){
			
			pstmt.setInt(1, model.getKey());
			pstmt.executeUpdate();
			status = true;
		}catch (SQLException e) {
			System.out.println(e.getMessage());
		}
	return status;	
	}
	//Update
	public boolean update(Resident model) {
		boolean status = false;
		String query = "UPDATE resident SET first_name = ?, last_name = ?, id = ? WHERE key = ?";
		
		try (Connection conn = helper.getConnection();
				 PreparedStatement pstmt = conn.prepareStatement(query)){
			
			pstmt.setString(1, model.getFirstName());
			pstmt.setString(2, model.getlastName());
			pstmt.setInt(3, model.getId());
			pstmt.setInt(4, model.getKey());
		    pstmt.executeUpdate();
		    status = true;
			
		}catch (SQLException e) {
			System.out.println(e.getMessage());
		}
		return status;
	}
}	
*/





