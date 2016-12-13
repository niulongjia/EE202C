#include <iostream>
#include <string>
#include <fstream>
#include <queue>
#include <utility>
#include <cmath>
#include <stdio.h>
#include "floatfann.h"
#include "parameters_listener.h"
#include <mraa/aio.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
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

	fann_type *calc_out;
  fann_type input[coefficients_num];
	
  ann = fann_create_from_file(output_neuro_file); // neuro-network

  float value;
	string line;


	int count=0;
 
	
  struct stat attr;
	long long int last_modified_time = 0;
	while (true)
	{
		int sign=stat(test_data_file, &attr);
		if (sign>=0 && attr.st_mtime > last_modified_time)
		{
			  //cout<<"status:"<<stat(test_data_file, &attr)<<endl;
					last_modified_time = attr.st_mtime;
					cout << "we find a change in file:" << test_data_file <<endl;
					cout << ctime(&attr.st_mtime);
					// st_mtime is seconds since 1970/01/01 00:00:00
					cout << attr.st_mtime << endl;

			   // begin reading test data and make predictions
				  std::ifstream myfile(test_data_file);
				  std::ofstream outfile(prediction_result_file);
				  std::ofstream outfile_html(prediction_result_html_file);
				   count=0;
				   while (myfile >> value)
					{
						input[count] = value;
						count++;
					}
					priority_queue< INFO, vector<INFO>, comp > q;
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
					if ((calc_out[4]>0.4 && calc_out[3]>0.6) || calc_out[4]>0.5 )state1="WALK";
					else if ((calc_out[1]>0.2 && calc_out[1]<=0.4 && calc_out[2]>=0 && calc_out[0]>0.5) || (calc_out[1]<0 && calc_out[1]<=calc_out[0] && calc_out[1]<=calc_out[5] && calc_out[1]<=calc_out[4]))  state1="READ";
					else if (calc_out[0]>0.5 && calc_out[3]>0.5 && calc_out[0]>calc_out[3]) state1="COOK";
					else if (calc_out[5]>0.05 && calc_out[5]<0.15 && calc_out[0]>0.5 && calc_out[1]<0.5 && calc_out[2]<0.5 && calc_out[3]<0.5 && calc_out[4]<0.5) state1="GROOM";
					else if (calc_out[1]>0.65 && calc_out[2]>0.2) state1="REST";
					else if (calc_out[3]>0.25 && calc_out[0]<0.3 && calc_out[1]<0.3  && calc_out[2]>0.7&& calc_out[4]<0.3 && calc_out[5]<0.3) state1="TYPE";

					else
					{
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
							{ state2="GROOM"; break;}
						}
						
					}
  
          	// setting the threshold of unknow state
          			if(MAX1.confidence < 0.1) 
          			{
          				state1 = "UNKNOWN";
          				//MAX1.confidence = 0;
          			}
          
          			if(MAX2.confidence < 0.1)
          			{
          				state2 = "UNKNOWN";
          				//MAX2.confidence = 0;
          			}
          		cout<< state1 <<":"<< MAX1.confidence << "   "<< state2 << ":" << MAX2.confidence << endl;
				outfile_html<< "<html><head><title>Temporary</title><meta http-equiv='refresh' content='1' /></head><body><h1>" << state1 << "</h1></body></html>" << endl;
				myfile.close();
				outfile.close();
		}
	}
 
	
    
    fann_destroy(ann);
    return 0;
}

