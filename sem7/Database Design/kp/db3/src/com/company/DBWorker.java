package com.company;

import java.sql.*;
import java.text.ParseException;
import java.util.Calendar;
import java.util.Date;

public class DBWorker {

    private final String URL = "jdbc:postgresql://localhost:5432/hospitaldb";
    private final String USER = "mikhail";
    private final String PASSWORD = "need4you";

    private Connection connection = null;
    private PreparedStatement preparedStatement = null;

    public Connection getConnection() {
        return connection;
    }

    public DBWorker() {
        try {
            Class.forName("org.postgresql.Driver");
            connection = DriverManager.getConnection(URL, USER, PASSWORD);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    ResultSet showAppointmentsToDoctor(int employee_id, java.sql.Date date) {
        String query = "SELECT employee_id, patient_id, appointment_time, free FROM patients_appointment " +
                "WHERE (employee_id = ? AND DATE(appointment_time) = ?);";
        ResultSet resultSet = null;
        try {
            preparedStatement = connection.prepareStatement(query);
            preparedStatement.setInt(1, employee_id);
            preparedStatement.setDate(2, date);
            resultSet = preparedStatement.executeQuery();
            connection.close();
            return resultSet;

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return resultSet;
    }

    public boolean insertAppointment(int employeeId, java.sql.Timestamp beginTime, java.sql.Timestamp endTime) {
        java.text.SimpleDateFormat df = new java.text.SimpleDateFormat("HH:mm");
        java.sql.Timestamp curTime = beginTime;
        int appointmentDuration = 15;
        Calendar cal = Calendar.getInstance();
        cal.setTime(beginTime);
        System.out.println(beginTime);
        System.out.println(endTime);
        curTime.setTime(curTime.getTime() + ((15 * 60)* 1000));
        System.out.println(curTime);
        String query = "insert into patients_appointment(employee_id, patient_id, free, appointment_time)" +
                " values(?, null, 't', ?);";
        try {
            PreparedStatement ps = connection.prepareStatement(query);
            while (curTime.before(endTime)) {
                ps.setInt(1, employeeId);
                ps.setTimestamp(2, curTime);
                curTime.setTime(curTime.getTime() + ((15 * 60) * 1000));
                ps.addBatch();
                ps.clearParameters();
            }
            ps.executeBatch();
        }
        catch (SQLException e) {
            e.printStackTrace();
            return false;
        } finally {
            if (connection != null) {
                try {
                    connection.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }

        return true;
    }

    public int updateEmployee(int oldEmployeetId, int newEmployeeId, java.sql.Date date) {
        System.out.println(oldEmployeetId);
        String query = "UPDATE patients_appointment set employee_id = ? " +
                "where (employee_id = ? and date(appointment_time) = ?);";
        int result = 0;
        try {
            preparedStatement = connection.prepareStatement(query);
            preparedStatement.setInt(1, newEmployeeId);
            preparedStatement.setInt(2, oldEmployeetId);
            preparedStatement.setDate(3, date);
            System.out.println(date);
            result = preparedStatement.executeUpdate();
        }
        catch (SQLException e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                try {
                    connection.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
        return result;
    }

    public int deleteDoctorAppointmentsOnDate(int employee_id, java.sql.Timestamp timeBegin, java.sql.Timestamp timeEnd) {
        String query = "delete from patients_appointment where (employee_id = ? and appointment_time between ? and ?);";
        try {
            preparedStatement = connection.prepareStatement(query);
            preparedStatement.setInt(1, employee_id);
            preparedStatement.setTimestamp(2, timeBegin);
            preparedStatement.setTimestamp(3, timeEnd);
            preparedStatement.execute();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                try {
                    connection.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
        return 1;
    }

    public boolean dismiss_employee(int employee_id) {
        String query = "{? = call dismiss_employee(?)}";
        boolean res = false;
        try {
            CallableStatement cs = connection.prepareCall(query);
            cs.setInt(1, employee_id);
            cs.registerOutParameter(2, Types.BOOLEAN);
            cs.execute();
            res = cs.getBoolean(2);
            cs.close();
            System.out.println(res);
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                try {
                    connection.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
        return res;
    }
}