package com.example.niulongjia.preciseclassificationapp;

/**
 * Created by niulongjia on 2016/11/19.
 */

public class ExchangeMessage
{
    //"REST", "READ", "COOK", "TYPE" ,"WALK","UNKNOWN"
    public int rest;
    public int read;
    public int cook;
    public int type;
    public int walk;
    public int groom;
    public int unknown;
    ExchangeMessage(int rest,int read,int cook,int type,int walk, int groom, int unknown)
    {
        this.rest=rest;
        this.read=read;
        this.cook=cook;
        this.type=type;
        this.walk=walk;
        this.groom=groom;
        this.unknown=unknown;
    }
}
