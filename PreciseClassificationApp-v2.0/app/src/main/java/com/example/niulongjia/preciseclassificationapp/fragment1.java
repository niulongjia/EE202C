package com.example.niulongjia.preciseclassificationapp;


import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.support.v4.view.ViewPager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import org.greenrobot.eventbus.EventBus;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.List;
import java.util.Vector;


/**
 * A simple {@link Fragment} subclass.
 */
public class fragment1 extends Fragment {
    Handler uiHandler = new Handler();

    Document siteDoc;
    String stateString="";
    Elements p;

    Button button;
    TextView textView;
    ImageView imageView;

    // need to change this every time !
    // need to connect android phone with wifi !
    String URL="http://131.179.1.199/prediction_update.html";

    //"COOK", "READ", "REST", "TYPE" ,"WALK", "GROOM", "UNKNOWN"
    int rest=0;
    int read=0;
    int cook=0;
    int type=0;
    int walk=0;
    int groom=0;
    int unknown=0;

    Handler handler = new Handler();
    public void startHandler()
    {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                new siteGetter().execute();
                startHandler();
            }
        },5000);

    }

    private final static int INTERVAL = 5000; //5 seconds
    Handler mHandler = new Handler();

    public Runnable mHandlerTask = new Runnable()
    {
        @Override
        public void run() {
            new siteGetter().execute();
            mHandler.postDelayed(mHandlerTask, INTERVAL);
        }
    };
    public void startRepeatingTask()
    {
        mHandlerTask.run();
    }
    public void stopRepeatingTask()
    {
        mHandler.removeCallbacks(mHandlerTask);
    }


    public fragment1() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view=inflater.inflate(R.layout.layout_fragment1,container,false);

        button= (Button) view.findViewById(R.id.button);
        textView = (TextView) view.findViewById(R.id.textView2);
        imageView=(ImageView)view.findViewById(R.id.imageView);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //new siteGetter().execute();
                textView.setText("reset");
            }
        });


        // The first way to execute asyncTask several times
         startHandler();

        // The second way to execute asyncTask several times
        // http://stackoverflow.com/questions/6207362/how-to-run-an-async-task-for-every-x-mins-in-android
        //startRepeatingTask();
        return view;
    }


    private class siteGetter extends AsyncTask< Void, Void, String>
    {
        //String a;
        @Override
        protected String doInBackground(Void... voids)
        {
            try
            {
                Log.d("debugMsg","before");
                //cnt=100;

                // How to handle if we can not connect?
                siteDoc = Jsoup.connect(URL).userAgent("Mozilla").get();
                //cnt++;
                //p = siteDoc.getElementsByTag("p");
                p=siteDoc.select("h1");
                stateString=p.first().text();

                Log.d("debugMsg","after");

            }
            catch (IOException ex)
            {
                //cnt++;
                ex.printStackTrace();}
            return stateString;
        }

        @Override
        protected void onPostExecute(final String stateString)
        {
            /*
            MainActivity.this.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    textView.setText(a);
                }
            });
            */
            Log.d("debugMsg3","onPostExecute");

            //"REST", "READ", "COOK", "TYPE" ,"WALK", "GROOM", "UNKNOWN"
            getActivity().runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    textView.setText(stateString);

                    // images must be stored in drawable folder to preserve resolution.
                    if (stateString.equals("REST")) {
                        imageView.setImageResource(R.drawable.pic_rest);
                        rest++;
                    }
                    else if (stateString.equals("READ")) {
                        imageView.setImageResource(R.drawable.pic_read);
                        read++;
                    }
                    else if (stateString.equals("COOK")) {
                        imageView.setImageResource(R.drawable.pic_cook);
                        cook++;
                    }
                    else if (stateString.equals("TYPE")) {
                        imageView.setImageResource(R.drawable.pic_type);
                        type++;
                    }
                    else if (stateString.equals("WALK")) {
                        imageView.setImageResource(R.drawable.pic_walk);
                        walk++;
                    }
                    else if (stateString.equals("GROOM")) {
                        imageView.setImageResource(R.drawable.pic_groom);
                        groom++;
                    }
                    else if (stateString.equals("UNKNOWN")) {
                        imageView.setImageResource(R.drawable.pic_unknown);
                        unknown++;
                    }
                    else if (stateString.length()>0) imageView.setImageResource(R.drawable.pic_error);
                }
            });


            EventBus.getDefault().post(new ExchangeMessage(
                    rest,read,cook,type,walk,groom, unknown
            ));
            //textView.setText(Integer.toString(cnt));
        }
    }

}
