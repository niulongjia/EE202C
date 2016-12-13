package com.example.niulongjia.preciseclassificationapp;


import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.components.Description;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.highlight.Highlight;
import com.github.mikephil.charting.listener.OnChartValueSelectedListener;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;

import java.util.ArrayList;

import static android.R.attr.value;
import static com.github.mikephil.charting.components.Legend.LegendForm.CIRCLE;
import static java.sql.Types.FLOAT;
import static java.sql.Types.INTEGER;

/*
    These contents about pieChart can be found on:
    https://github.com/PhilJay/MPAndroidChart
*/
public class fragment2 extends Fragment {

    //"REST", "READ", "COOK", "TYPE" ,"WALK", "GROOM", "UNKNOWN"
    public int[] yData={0,0,0,0,0,0,0};
    public String[] xData={"REST","READ","COOK","TYPE","WALK","GROOM","UNKNOWN"};



    public Button button;
    public PieChart pieChart;

    //"REST", "READ", "COOK", "TYPE" ,"WALK","UNKNOWN"
    int rest=0;
    int read=0;
    int cook=0;
    int type=0;
    int walk=0;
    int groom=0;
    int unknown=0;

    int total=0;
    public fragment2() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState)
    {
        View view=inflater.inflate(R.layout.layout_fragment2,container,false);
        button=(Button)view.findViewById(R.id.button2);
        pieChart = (PieChart)view.findViewById(R.id.pieChart);


        //addDataSet();
        /*
        pieChart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                addDataSet();
            }
        });
        */

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                addDataSet();
            }
        });



        pieChart.setOnChartValueSelectedListener(new OnChartValueSelectedListener() {
            @Override
            public void onValueSelected(Entry e, Highlight h) {

                Log.d("debugMsg4",h.toString());

                //"REST", "READ", "COOK", "TYPE" ,"WALK","UNKNOWN"
                Log.d("debugMsg4","REST:"+Integer.toString(rest)+
                                 " READ:"+Integer.toString(read)+
                                 " COOK:"+Integer.toString(cook)+
                                 " TYPE:"+Integer.toString(type)+
                                 " WALK:"+Integer.toString(walk)+
                                " GROOM:"+Integer.toString(groom)+
                                 " UNKNOWN:"+Integer.toString(unknown));


                int index = (int)h.getX();
                int value = (int)h.getY();
                Log.d("debugMsg4","h.getX():"+Integer.toString(index)+" h.getY():"+Integer.toString(value));

                String stateName = xData[index];
                Toast.makeText(getActivity(),"State: "+stateName + "\n" + "Number: " + Integer.toString(value), Toast.LENGTH_LONG).show();

            }

            @Override
            public void onNothingSelected() {

            }
        });

        // Inflate the layout for this fragment
        return view;
    }

    @Override
    public void onStart() {
        super.onStart();
        EventBus.getDefault().register(this);
    }

    @Override
    public void onStop() {
        EventBus.getDefault().unregister(this);
        super.onStop();

    }
    @Subscribe
    public void onEvent(final ExchangeMessage exchangeMessage)
    {
        //"REST", "READ", "COOK", "TYPE" ,"WALK","UNKNOWN"
        rest=exchangeMessage.rest;
        read=exchangeMessage.read;
        cook=exchangeMessage.cook;
        type=exchangeMessage.type;
        walk=exchangeMessage.walk;
        groom=exchangeMessage.groom;
        unknown=exchangeMessage.unknown;

        Log.d("debugMsg3","walk:"+Integer.toString(walk));
        /*
        rest (Color.GRAY);
        read (Color.BLUE);
        cook (Color.RED);
        type (Color.GREEN);
        walk (Color.YELLOW);
        groom (Color.BLACK);
        unknown (Color.MAGENTA);
        */
        yData[0]=rest;
        yData[1]=read;
        yData[2]=cook;
        yData[3]=type;
        yData[4]=walk;
        yData[5]=groom;
        yData[6]=unknown;
        total=rest+read+cook+type+walk+groom+unknown;
    }
    public void addDataSet()
    {
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                Description description = new Description();
                description.setText("Test Pie Chart Description!");
                pieChart.setDescription(description);

                pieChart.setRotationEnabled(true);
                pieChart.setHoleRadius(10f);
                pieChart.setTransparentCircleAlpha(0);
                pieChart.setCenterText("cool");
                pieChart.setCenterTextSize(5f);
                pieChart.setDrawEntryLabels(true);

                //pieChart.invalidate();
                Log.d("debugMsg3","In addDataSet");

                ArrayList<PieEntry> yEntry=new ArrayList<>();
                ArrayList<String> xEntry=new ArrayList<>();

                for (int i=0;i<yData.length;i++)
                {
                    yEntry.add(new PieEntry(yData[i],i));
                    //xEntry.add(xData[i]);
                }

                //create slices of pie chart.
                PieDataSet pieDataSet=new PieDataSet(yEntry,"States");
                pieDataSet.setSliceSpace(5);
                pieDataSet.setValueTextSize(10);

                //add colors to slices of pie chart
                ArrayList<Integer> colors = new ArrayList<>();
                colors.add(Color.GRAY);
                colors.add(Color.BLUE);
                colors.add(Color.RED);
                colors.add(Color.GREEN);
                colors.add(Color.YELLOW);
                colors.add(Color.BLACK);
                colors.add(Color.MAGENTA);

                pieDataSet.setColors(colors);

                //add legends to the chart
                Legend legend = pieChart.getLegend();
                legend.setForm(Legend.LegendForm.CIRCLE);


                //create pie chart object

                PieData pieData=new PieData(pieDataSet);

                pieChart.setData(pieData);
                pieChart.invalidate();

            }
        });

    }

}
