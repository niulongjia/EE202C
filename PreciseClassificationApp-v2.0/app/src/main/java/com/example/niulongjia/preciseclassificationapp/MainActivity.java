package com.example.niulongjia.preciseclassificationapp;

import android.os.AsyncTask;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

//import org.w3c.dom.Document;
//import org.jsoup.*;
import org.jsoup.Jsoup;
import org.jsoup.helper.Validate;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.URLConnection;
import java.util.List;
import java.util.Vector;

// User must use the same network with computer and Intel Edison !
// Do not use 4G !

/*
* several Problems:
* 1. when navigating from last page back to first page, it will reset timer. why?
* 2. sometimes app will crash. why?
* */
public class MainActivity extends AppCompatActivity
{

    public SwipeAdapter mSwipeAdapter;
    public ViewPager viewPager;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // swipe to show three fragments
        // fragment1 --> state string and picture
        // fragment2 --> pie chart
        // fragment3 --> creaters
        List<Fragment> fragments=new Vector<Fragment>();
        fragments.add(Fragment.instantiate(this,fragment1.class.getName()));
        fragments.add(Fragment.instantiate(this,fragment2.class.getName()));
        fragments.add(Fragment.instantiate(this,fragment3.class.getName()));
        mSwipeAdapter=new SwipeAdapter(getSupportFragmentManager(),fragments);
        viewPager=(ViewPager)findViewById(R.id.view_pager);
        viewPager.setAdapter(mSwipeAdapter);
    }


    @Override
    protected void onResume()
    {
        super.onResume();
    }
}
