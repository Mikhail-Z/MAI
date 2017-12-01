package com.company;

import java.sql.*;
import java.text.ParseException;
import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;


public class Main {

    public static void main(String[] args) {
        int argsCount = args.length;
        if (argsCount >= 1) {
            DBWorker worker = new DBWorker();
            String command = args[0];
            if (command.equals("\\s")) {
                if (args.length != 3)
                    System.out.println("Wrong arguments of command. To see help type \\h");
                try {
                    int employee_id = Integer.parseInt(args[1]);
                    DateFormat df = new SimpleDateFormat("dd.MM.yyyy");
                    Date appointment_date = df.parse(args[2]);
                    java.sql.Date sqlDate = new java.sql.Date(appointment_date.getTime());
                    ResultSet rs = worker.showAppointmentsToDoctor(employee_id, sqlDate);

                }
                catch (ParseException e) {
                    e.printStackTrace();
                }
            }
            else if (command.equals("\\u")) {
                int res = 0;
                if (args.length != 4) {
                    System.out.println("Wrong arguments of command. To see help type \\h");
                    return;
                }
                try {
                    int oldEmployeeId = Integer.parseInt(args[1]);
                    int newEmployeeId = Integer.parseInt(args[2]);
                    DateFormat df = new SimpleDateFormat("dd.MM.yyyy");
                    Date appointment_date = df.parse(args[3]);
                    java.sql.Date sqlDate = new java.sql.Date(appointment_date.getTime());
                    res = worker.updateEmployee(oldEmployeeId, newEmployeeId, sqlDate);
                } catch (ParseException e) {
                    e.printStackTrace();
                } finally {
                    if (res > 0)
                        System.out.println("Done");
                    else
                        System.out.println("Operation cancelled: wrong format of arguments. See help.");
                }
            }
            else if (command.equals("\\i")) {
                boolean res = false;
                if (args.length != 5) {
                    System.out.println("Wrong arguments of command. To see help type \\h");
                    return;
                }
                int employee_id = Integer.parseInt(args[1]);
                java.sql.Timestamp beginTime = java.sql.Timestamp.valueOf(args[2]+" "+args[3]);
                java.sql.Timestamp endTime = java.sql.Timestamp.valueOf(args[2]+" "+args[4]);
                res = worker.insertAppointment(employee_id, beginTime, endTime);
                if (res)
                    System.out.println("Done");
                else
                    System.out.println("Operation cancelled: wrong format of arguments. See help.");
            }
            else if (command.equals("\\d")) {
                if (args.length != 5) {
                    System.out.println("Wrong arguments of command. To see help type \\h");
                    return;
                }
                int employee_id = Integer.parseInt(args[1]);
                java.sql.Timestamp beginTime = java.sql.Timestamp.valueOf(args[2]+" "+args[3]);
                java.sql.Timestamp endTime = java.sql.Timestamp.valueOf(args[2]+" "+args[4]);
                worker.deleteDoctorAppointmentsOnDate(employee_id, beginTime, endTime);

            }
            else if (command.equals("\\dismiss")) {
                if (args.length != 2) {
                    System.out.println("Wrong arguments of command. To see help type \\h");
                    return;
                }
                int employeeId = Integer.parseInt(args[1]);
                if (worker.dismiss_employee(employeeId))
                    System.out.println("Done.");
            }
            else if (command.equals("\\h")) {
                String s_description = new String ("\\s is used to show information appointment of certain" +
                        " doctor on certain date. Usage:\n\\s 5 19.09.2016\n where 5 is id of employee" +
                        " and 19.09.2016 is date on which you want to see appointments.");
                String u_description = new String("\\u is used to update information in current database.\n" +
                        "Usage:\n\\u 5 18 20.12.2014 \nwhere 5 is id of old employee," +
                        " 18 is id of new employee and 18.12.2014 is date on which you want to update employee.");
                String i_description = new String("\\i is used to insert new rows into table. Usage:\n" +
                        "\\i 2 2016-04-16 13:20:00.0 18.30:00.0\nwhere 2 is id of employee, second argument is date and third one" +
                        " is beginning of time interval fourth one is end of time interval");
                String d_description = new String("\\d is used to delete rows with appointment of certain employee" +
                        "on certain date. Usage:\n\\d 2 2016-10-16 10:30:00.0 13:30:00.0");
                String dismiss_description = new String("Dismiss employee. Note,that if there are appointments" +
                        "to him in the future, operation will be cancelled. So before this use update command to set new employee");
                System.out.println(s_description);
                System.out.println(u_description);
                System.out.println(i_description);
                System.out.println(d_description);
                System.out.println(dismiss_description);
            }
            else {
                System.out.println("Wrong command. Use \\h for help.");
            }
        }
    }

}