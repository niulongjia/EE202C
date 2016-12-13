#include <iostream>
#include <unistd.h>
#include <mraa/aio.h>
#include <stdio.h>
#include "floatfann.h"
#include <string>
#include <fstream>
#include <queue>
#include <utility>
#include <cmath>
#include "parameters.h"
using namespace std;

struct INFO
{
	int index;
	float confidence;
	INFO(int i, float conf)
	{
		index=i;
		confidence=conf;
	}
	INFO()
	{
	  index=-1;
	  confidence=-1;
	}
};

struct comp
{
	bool operator()( INFO info1, INFO info2 )
	{
	   if (info1.confidence < info2.confidence) return true;
	   else return false;
	}
};
int main()
{
    int i;
    //int location;
    //float max=-100;
    INFO MAX1;
    INFO MAX2;

    struct fann *ann;
    
	// int coefficients_num=15; // 15 coefficients
	// int states_num=2; // 2 states {READ, REST}
	fann_type *calc_out;
  fann_type input[coefficients_num];
	
  ann = fann_create_from_file(output_neuro_file); // neuro-network
	// During testing
	// inputs are coefficients
	// outputs are states.

  //std::cout<<"global_variable: "<<global_variable<<std::endl; 
	//std::cout<<"coefficients_num:"<<coefficients_num<<endl;
  float value;
	string line;
	std::ifstream myfile(test_data_file);
  std::ofstream outfile(prediction_results_file);
	int count=0;
 
  	
	while (myfile >> value)
	{
		count=count%coefficients_num;
		//std::cout<<"value:"<<value<<" ";
    //std::cout<<endl;
		input[count]=abs(value);
		count++;
		if (count>=coefficients_num)
		{
			priority_queue< INFO, vector<INFO>, comp > q;
      
      
			//for (i=0;i<count;i++) cout<<input[i]<<" ";
      //std::cout<<endl;
			count=0;
			calc_out = fann_run(ann, input);
			// cal_out stores the predicted states!
      //max = -100;
			for (i = 0; i < states_num; i++) 
			{     
				INFO info(i,calc_out[i]);
				q.push(info);
			}
      std::cout<<"COOK:"<<calc_out[0]<<" READ:"<<calc_out[1]<<" REST:"<<calc_out[2]<<" TYPE:"<<calc_out[3]<<" WALK:"<<calc_out[4]<<" GROOM:"<<calc_out[5]<<endl;
			INFO MAX1 = q.top();
			q.pop();
			INFO MAX2 = q.top();
			q.pop();
				/*
				cook read rest type walk groom
				1 0 0 0	0 0
				0 1 0 0	0 0
				0 0 1 0	0 0
				0 0 0 1	0 0
				0 0 0 0 1 0
				0 0 0 0 0 1					
				*/
			string state1="";
			string state2="";
			switch(MAX1.index)
			{
				case 0:
				{  state1="COOK";	break;	}
				
				case 1:
				{ state1="READ"; break; }
				
				case 2:
				{ state1="REST"; break; }
			
				case 3:
				{ state1="TYPE"; break; }
        
				case 4:
				{ state1="WALK"; break;}
				
				case 5:
				{ state1="GROOM"; break;}
			}

			switch(MAX2.index)
			{
				case 0:
				{ state2="COOK"; break;	}
				
				case 1:
				{ state2="READ";break; }
				
				case 2:
				{ state2="REST";break; }
			
				case 3:
				{ state2="TYPE"; break; }

				case 4:
				{ state2="WALK";break; }
				
				case 5:
				{ state2="GROOM";break; }
			}
	// setting the threshold of unknow state
			if(MAX1.confidence < 0.15) 
			{
				state1 = "UNKNOWN";
				//MAX1.confidence = 0;
			}

			if(MAX2.confidence < 0.15)
			{
				state2 = "UNKNOWN";
				//MAX2.confidence = 0;
			}
			cout<< state1 <<":"<< MAX1.confidence << "   "<< state2 << ":" << MAX2.confidence << endl;
			outfile<<state1<<" + "<<state2<<endl;
			//outfile<<state1<<endl;
		}
		

	}
    myfile.close();
    fann_destroy(ann);
    return 0;
}

