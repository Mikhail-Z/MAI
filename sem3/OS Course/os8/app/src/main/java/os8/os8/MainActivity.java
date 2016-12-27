package os8.os8;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;


/*public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    final int MENU_RESET_ID = 1;
    final int MENU_QUIT_ID = 2;

    EditText etNum1;
    EditText etNum2;

    Button btnAdd;
    Button btnSub;
    Button btnMult;
    Button btnDiv;
    Button btnPow;
    Button btnFact;
    Button btnSqr;
    Button btnSqrt;

    TextView tvResult;

    String oper = "";

    /** Called when the activity is first created. */

    //@Override
    /*public int myFact(int num1) {
        if (num1 == 1)
            return 1;
        else return num1*myFact(--num1);
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // ������� ��������
        etNum1 = (EditText) findViewById(R.id.etNum1);
        etNum2 = (EditText) findViewById(R.id.etNum2);

        btnAdd = (Button) findViewById(R.id.btnAdd);
        btnSub = (Button) findViewById(R.id.btnSub);
        btnMult = (Button) findViewById(R.id.btnMult);
        btnDiv = (Button) findViewById(R.id.btnDiv);

        btnPow = (Button) findViewById(R.id.btnPow);
        btnFact = (Button) findViewById(R.id.btnFact);
        btnSqr = (Button) findViewById(R.id.btnSqr);
        btnSqrt = (Button) findViewById(R.id.btnSqrt);

        tvResult = (TextView) findViewById(R.id.tvResult);

        // ����������� ����������
        btnAdd.setOnClickListener(this);
        btnSub.setOnClickListener(this);
        btnMult.setOnClickListener(this);
        btnDiv.setOnClickListener(this);

        btnPow.setOnClickListener(this);
        btnFact.setOnClickListener(this);
        btnSqr.setOnClickListener(this);
        btnSqrt.setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {
        // TODO Auto-generated method stub
        float num1 = 0;
        float num2 = 0;
        float result = 0;

        // ��������� ���� �� �������
        if (TextUtils.isEmpty(etNum1.getText().toString())
                || TextUtils.isEmpty(etNum2.getText().toString())) {
            return;
        }

        // ������ EditText � ��������� ���������� �������
        num1 = Float.parseFloat(etNum1.getText().toString());
        num2 = Float.parseFloat(etNum2.getText().toString());

        // ���������� ������� ������ � ��������� ��������������� ��������
        // � oper ����� ��������, ����� ����� ������������ � ������
        switch (v.getId()) {
            case R.id.btnAdd:
                oper = "+";
                result = num1 + num2;
                break;
            case R.id.btnSub:
                oper = "-";
                result = num1 - num2;
                break;
            case R.id.btnMult:
                oper = "*";
                result = num1 * num2;
                break;
            case R.id.btnDiv:
                oper = "/";
                result = num1 / num2;
                break;
            case R.id.btnPow:
                oper = "^";
                result = (float)Math.pow(num1, num2);
                break;
            case R.id.btnFact:
                oper = "!";
                result = myFact((int)num1);
                break;
            case R.id.btnSqr:
                oper = "^2";
                result = (float)Math.pow(num1,2);
                break;
            case R.id.btnSqrt:
                oper = "^(1/2)";
                result = (float)Math.pow(num1,0.5);
                break;
            default:
                break;
        }

        // ��������� ������ ������
        tvResult.setText(num1 + " " + oper + " " + num2 + " = " + result);
    }

    // �������� ����
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
// TODO Auto-generated method stub
        menu.add(0, MENU_RESET_ID, 0, "Reset");
        menu.add(0, MENU_QUIT_ID, 0, "Quit");
        return super.onCreateOptionsMenu(menu);
    }

    // ��������� ������� �� ������ ����
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
// TODO Auto-generated method stub
        switch (item.getItemId()) {
            case MENU_RESET_ID:
// ������� ����
                etNum1.setText("");
                etNum2.setText("");
                tvResult.setText("");
                break;
            case MENU_QUIT_ID:
// ����� �� ����������
                finish();
                break;
        }
        return super.onOptionsItemSelected(item);
    }
}*/
    public class MainActivity extends AppCompatActivity implements View.OnClickListener {

        final int MENU_RESET_ID = 1;
        final int MENU_QUIT_ID = 2;

        EditText etNum1;
        EditText etNum2;

        Button btnAdd;
        Button btnSub;
        Button btnMult;
        Button btnDiv;
        Button btnPow;
        Button btnFact;
        Button btnSqr;
        Button btnSqrt;
        Button btnLog;
        Button btnExp;
        Button btnSin;
        Button btnCos;


        TextView tvResult;

        String oper = "";

        /**
         * Called when the activity is first created.
         */

        //@Override
        public int myFact(int num1) {
            if (num1 == 1)
                return 1;
            else return num1 * myFact(--num1);
        }

        @Override
        public void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);

            etNum1 = (EditText) findViewById(R.id.etNum1);
            etNum2 = (EditText) findViewById(R.id.etNum2);

            btnAdd = (Button) findViewById(R.id.btnAdd);
            btnSub = (Button) findViewById(R.id.btnSub);
            btnMult = (Button) findViewById(R.id.btnMult);
            btnDiv = (Button) findViewById(R.id.btnDiv);

            btnPow = (Button) findViewById(R.id.btnPow);
            btnFact = (Button) findViewById(R.id.btnFact);
            btnSqr = (Button) findViewById(R.id.btnSqr);
            btnSqrt = (Button) findViewById(R.id.btnSqrt);

            btnLog = (Button) findViewById(R.id.btnLog);
            btnExp = (Button) findViewById(R.id.btnExp);
            btnSin = (Button) findViewById(R.id.btnSin);
            btnCos = (Button) findViewById(R.id.btnCos);

            tvResult = (TextView) findViewById(R.id.tvResult);

            btnAdd.setOnClickListener(this);
            btnSub.setOnClickListener(this);
            btnMult.setOnClickListener(this);
            btnDiv.setOnClickListener(this);

            btnPow.setOnClickListener(this);
            btnFact.setOnClickListener(this);
            btnSqr.setOnClickListener(this);
            btnSqrt.setOnClickListener(this);

            btnLog.setOnClickListener(this);
            btnExp.setOnClickListener(this);
            btnSin.setOnClickListener(this);
            btnCos.setOnClickListener(this);

        }

        @Override
        public void onClick(View v) {
            // TODO Auto-generated method stub
            float num1 = 0;
            float num2 = 0;
            float result = 0;
            Boolean un = false;


            if (TextUtils.isEmpty(etNum1.getText().toString())
                    && TextUtils.isEmpty(etNum2.getText().toString())) {
                return;
            }

            if (TextUtils.isEmpty(etNum1.getText().toString())
                    || TextUtils.isEmpty(etNum2.getText().toString())) {
                un = !un;
                if (TextUtils.isEmpty(etNum1.getText().toString())) {
                    num1 = Float.parseFloat(etNum2.getText().toString());
                }else{
                    num1 = Float.parseFloat(etNum1.getText().toString());
                }
            } else {
                num1 = Float.parseFloat(etNum1.getText().toString());
                num2 = Float.parseFloat(etNum2.getText().toString());
            }

            switch (v.getId()) {
                case R.id.btnAdd:
                    if (!un) {
                        oper = "+";
                        result = num1 + num2;
                        tvResult.setText(num1 + " " + oper + " " + num2 + " = " + result);
                    } else {
                        // Сообщение об ошибке, не введено второе число
                        return;
                    }
                    break;
                case R.id.btnSub:
                    if (!un) {
                        oper = "-";
                        result = num1 - num2;
                        tvResult.setText(num1 + " " + oper + " " + num2 + " = " + result);
                    } else {
                        // Сообщение об ошибке, не введено второе число
                        return;
                    }
                    break;
                case R.id.btnMult:
                    if (!un) {
                        oper = "*";
                        result = num1 * num2;
                        tvResult.setText(num1 + " " + oper + " " + num2 + " = " + result);
                    } else {
                        // Сообщение об ошибке, не введено второе число
                        return;
                    }
                    break;
                case R.id.btnDiv:
                    if (!un) {
                        oper = "/";
                        result = num1 / num2;
                        tvResult.setText(num1 + " " + oper + " " + num2 + " = " + result);
                    } else {
                        // Сообщение об ошибке, не введено второе число
                        return;
                    }
                    break;
                case R.id.btnPow:
                    if (!un) {
                        oper = "^";
                        result = (float) Math.pow(num1, num2);
                        tvResult.setText(num1 + " " + oper + " " + num2 + " = " + result);
                    } else {
                        // Сообщение об ошибке, не введено второе число
                        return;
                    }
                    break;
                case R.id.btnFact:
                    if (un) {
                        oper = "!";
                        result = myFact((int) num1);
                        tvResult.setText(num1 + " " + oper + " " + " = " + result);
                    }
                    else return;
                    break;
                case R.id.btnSqr:
                    if (un) {
                        oper = "^2";
                        result = (float) Math.pow(num1, 2);
                        tvResult.setText(num1 + " " + oper + " " + " = " + result);
                    }
                    else return;
                    break;
                case R.id.btnSqrt:
                    if (un) {
                        oper = "^(1/2)";
                        result = (float) Math.sqrt(num1);
                        tvResult.setText(num1 + " " + oper + " " + " = " + result);
                    }
                    else return;
                    break;
                case R.id.btnLog:
                    if (un) {
                        oper = "Ln ";
                        result = (float)Math.log(num1);
                        tvResult.setText(oper + num1 + " = " + result);
                    }
                    else return;
                    break;
                case R.id.btnExp:
                    if (un) {
                        oper = "e^";
                        result = (float)Math.exp(num1);
                        tvResult.setText(oper + num1 + " = " + result);
                    }
                    else return;
                    break;
                case R.id.btnSin:
                    if (un) {
                        oper = "Sin(";
                        result = (float)Math.sin(Math.toRadians(num1));
                        tvResult.setText(oper + num1 + ") = " + result);
                    }
                    else return;
                    break;
                case R.id.btnCos:
                    if (un) {
                        oper = "Cos(";
                        result = (float)Math.cos(Math.toRadians(num1));
                        tvResult.setText(oper + num1 + ") = " + result);
                    }
                    else return;
                    break;
                default: {
                    result = 0;
                }
                break;
            }

            /*if (!un)
                tvResult.setText(num1 + " " + oper + " " + num2 + " = " + result);
            else
                tvResult.setText(num1 + " " + oper + " " + " = " + result);*/
        }

        @Override
        public boolean onCreateOptionsMenu(Menu menu) {
// TODO Auto-generated method stub
            menu.add(0, MENU_RESET_ID, 0, "Reset");
            menu.add(0, MENU_QUIT_ID, 0, "Quit");
            return super.onCreateOptionsMenu(menu);
        }

        @Override
        public boolean onOptionsItemSelected(MenuItem item) {
// TODO Auto-generated method stub
            switch (item.getItemId()) {
                case MENU_RESET_ID:
                    etNum1.setText("");
                    etNum2.setText("");
                    tvResult.setText("");
                    break;
                case MENU_QUIT_ID:
                    finish();
                    break;
            }
            return super.onOptionsItemSelected(item);
        }
    }
