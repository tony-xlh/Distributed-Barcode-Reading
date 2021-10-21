package com.dynamsoft.dbrzeromq;

import androidx.appcompat.app.AppCompatActivity;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.dynamsoft.dbr.*;
import com.google.android.material.textfield.TextInputEditText;

import org.zeromq.SocketType;
import org.zeromq.ZMQ;
import org.zeromq.ZContext;


import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    private BarcodeReader reader;
    private TextView tv;
    private TextView idTv;
    private TextInputEditText ipEt;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        idTv=findViewById(R.id.idTextView);
        tv=findViewById(R.id.textView);
        ipEt=findViewById(R.id.ipTextEdit);
        initDBR();

    }

    public void connectButton_onClicked(View view){
        ZeroMQThread t = new ZeroMQThread();
        t.start();
    }

    private void initDBR(){
        try {
            reader = new BarcodeReader();
            DMDLSConnectionParameters dbrParameters = new DMDLSConnectionParameters();
            dbrParameters.organizationID = "200001";
            reader.initLicenseFromDLS(dbrParameters, new DBRDLSLicenseVerificationListener() {
                @Override
                public void DLSLicenseVerificationCallback(boolean isSuccessful, Exception e) {
                    if (!isSuccessful) {
                        e.printStackTrace();
                    }
                }
            });
            tv.setText("DBR version: "+reader.getVersion());
        } catch (BarcodeReaderException e) {
            e.printStackTrace();
        }
    }

    private byte[] DownloadImage(String url){
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(url).build();
        try (Response response = client.newCall(request).execute()) {
            return response.body().bytes();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public String decodeFile(byte[] data) {
        ArrayList<HashMap<String,Object>> resultList = new ArrayList<>();
        HashMap<String,Object> DecodingResult = new HashMap<String, Object>();
        long time0 = System.nanoTime();
        if (data!=null){
            try {
                TextResult[] results = reader.decodeFileInMemory(data,"");
                for (int i = 0; i < results.length; i++) {
                    TextResult result = results[i];

                    HashMap<String,Object> resultMap = new HashMap<String, Object>();
                    resultMap.put("barcodeText", result.barcodeText);
                    resultMap.put("barcodeFormat", result.barcodeFormatString);
                    resultMap.put("confidence", result.results[0].confidence);
                    resultMap.put("x1", result.localizationResult.resultPoints[0].x);
                    resultMap.put("y1", result.localizationResult.resultPoints[0].y);
                    resultMap.put("x2", result.localizationResult.resultPoints[1].x);
                    resultMap.put("y2", result.localizationResult.resultPoints[1].y);
                    resultMap.put("x3", result.localizationResult.resultPoints[2].x);
                    resultMap.put("y3", result.localizationResult.resultPoints[2].y);
                    resultMap.put("x4", result.localizationResult.resultPoints[3].x);
                    resultMap.put("y4", result.localizationResult.resultPoints[3].y);
                    resultList.add(resultMap);
                }
            }
            catch (Exception ex) {
                ex.printStackTrace();
            }
        }
        long time1 = System.nanoTime();
        long milliseconds = (long) ((time1-time0)*1e-6);
        DecodingResult.put("results", resultList);
        DecodingResult.put("elapsedTime", milliseconds);
        String jsonString = JSON.toJSONString(DecodingResult);
        return jsonString;
    }

    public class ZeroMQThread extends Thread{

        @Override
        public void run() {
            super.run();
            Log.d("DBR","Running ZeroMQ");
            try (ZContext context = new ZContext()) {
                Random r = new Random();
                int id = r.nextInt(10005);
                String ip = ipEt.getText().toString();
                Log.d("DBR",ip);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        idTv.setText("Consumer #"+id +" started.");
                    }
                });

                // Socket to talk to clients
                ZMQ.Socket consumerReceiver = context.createSocket(SocketType.PULL);
                consumerReceiver.connect("tcp://"+ip+":5557");
                ZMQ.Socket consumerSender = context.createSocket(SocketType.PUSH);
                consumerSender.connect("tcp://"+ip+":5558");
                Log.d("DBR","connecting done");
                while (true){
                    try{
                        String jsonString = consumerReceiver.recvStr();
                        Log.d("DBR",jsonString);
                        //Thread.sleep(1000);
                        JSONObject jsonObject = JSON.parseObject(jsonString);
                        JSONObject result = new JSONObject();
                        byte[] data = DownloadImage((String) jsonObject.get("url"));
                        String resultString = decodeFile(data);
                        result.put("consumer",id);
                        result.put("reading_result",JSON.parseObject(resultString));
                        result.put("session_id",jsonObject.get(("session_id")));
                        result.put("url",jsonObject.get(("url")));
                        String resultJSONString = result.toJSONString();
                        consumerSender.send(resultJSONString);
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                tv.setText(jsonString+"\n"+resultString);
                            }
                        });
                    } catch (Exception e) {
                        e.printStackTrace();
                    }

                }
            }
        }
    }
}